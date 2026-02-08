import json
import os
import uuid

import redis.asyncio as redis
import reflex as rx
from pydantic import BaseModel

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_CHANNEL = os.getenv("REDIS_CHANNEL", "reflex:example5")


class Product(BaseModel):
    id: int
    name: str
    price: float
    icon: str


class ExampleFiveState(rx.State):
    """Derived state synced through Redis Pub/Sub."""

    products: list[Product] = [
        Product(id=1, name="Neural Link Cable", price=49.99, icon="zap"),
        Product(id=2, name="Quantum Processor", price=899.0, icon="cpu"),
        Product(id=3, name="Holographic Display", price=249.5, icon="monitor"),
        Product(id=4, name="Bio-Metric Scanner", price=120.0, icon="fingerprint"),
    ]
    selected_product_id: int = 1
    quantity: int = 1
    discount_code: str = ""
    tax_rate: float = 0.0825

    session_id: str = ""
    connection_status: str = "disconnected"
    is_listening: bool = False
    last_message: str = "None"
    event_log: list[str] = []

    @rx.var
    def selected_product(self) -> Product:
        for p in self.products:
            if p.id == self.selected_product_id:
                return p
        return self.products[0]

    @rx.var
    def subtotal(self) -> float:
        return self.selected_product.price * self.quantity

    @rx.var
    def discount_percent(self) -> float:
        codes = {"REFLEX20": 0.2, "DEVMODE": 0.5, "SAVE10": 0.1}
        return codes.get(self.discount_code.upper(), 0.0)

    @rx.var
    def discount_amount(self) -> float:
        return self.subtotal * self.discount_percent

    @rx.var
    def tax_amount(self) -> float:
        return (self.subtotal - self.discount_amount) * self.tax_rate

    @rx.var
    def total(self) -> float:
        return self.subtotal - self.discount_amount + self.tax_amount

    def _build_payload(self) -> dict:
        return {
            "selected_product_id": self.selected_product_id,
            "quantity": self.quantity,
            "discount_code": self.discount_code,
            "tax_rate": self.tax_rate,
        }

    def _apply_payload(self, payload: dict):
        if "selected_product_id" in payload:
            self.selected_product_id = int(payload["selected_product_id"])
        if "quantity" in payload:
            self.quantity = max(1, int(payload["quantity"]))
        if "discount_code" in payload:
            self.discount_code = str(payload["discount_code"])
        if "tax_rate" in payload:
            self.tax_rate = float(payload["tax_rate"])

    def _log_event(self, message: str):
        self.event_log.insert(0, message)
        if len(self.event_log) > 6:
            self.event_log.pop()

    async def _publish_state(self, label: str, payload: dict):
        message = {
            "origin": self.session_id,
            "label": label,
            "payload": payload,
        }
        client = redis.from_url(REDIS_URL, decode_responses=True)
        try:
            await client.publish(REDIS_CHANNEL, json.dumps(message))
            async with self:
                self.last_message = f"Sent: {label}"
                self._log_event(self.last_message)
        except Exception as exc:
            async with self:
                self.connection_status = "error"
                self._log_event(f"Publish failed: {exc}")
        finally:
            await client.close()

    @rx.event(background=True)
    async def listen_redis(self):
        async with self:
            if self.is_listening:
                return
            if not self.session_id:
                self.session_id = uuid.uuid4().hex
            self.is_listening = True
            self.connection_status = "connecting"
            self.last_message = "Waiting for messages..."
        client = redis.from_url(REDIS_URL, decode_responses=True)
        pubsub = client.pubsub()
        try:
            await pubsub.subscribe(REDIS_CHANNEL)
            async with self:
                self.connection_status = "connected"
                self._log_event("Connected to Redis")
            async for message in pubsub.listen():
                if message.get("type") != "message":
                    continue
                try:
                    data = json.loads(message.get("data", "{}"))
                except json.JSONDecodeError:
                    async with self:
                        self._log_event("Ignored malformed message")
                    continue
                if data.get("origin") == self.session_id:
                    continue
                payload = data.get("payload", {})
                label = data.get("label", "Incoming update")
                async with self:
                    self._apply_payload(payload)
                    self.last_message = f"Received: {label}"
                    self._log_event(self.last_message)
        except Exception as exc:
            async with self:
                self.connection_status = "error"
                self._log_event(f"Connection error: {exc}")
        finally:
            try:
                await pubsub.unsubscribe(REDIS_CHANNEL)
                await pubsub.close()
            finally:
                await client.close()
                async with self:
                    self.is_listening = False

    @rx.event(background=True)
    async def select_product(self, val: str):
        async with self:
            if not self.session_id:
                self.session_id = uuid.uuid4().hex
            self.selected_product_id = int(val)
            payload = self._build_payload()
        await self._publish_state("Product changed", payload)

    @rx.event(background=True)
    async def change_quantity(self, val: float):
        async with self:
            if not self.session_id:
                self.session_id = uuid.uuid4().hex
            try:
                self.quantity = max(1, int(val))
            except (TypeError, ValueError):
                self.quantity = 1
            payload = self._build_payload()
        await self._publish_state("Quantity changed", payload)

    @rx.event(background=True)
    async def update_discount_code(self, code: str):
        async with self:
            if not self.session_id:
                self.session_id = uuid.uuid4().hex
            self.discount_code = code
            payload = self._build_payload()
        await self._publish_state("Discount code changed", payload)

    @rx.event(background=True)
    async def broadcast_state(self):
        async with self:
            if not self.session_id:
                self.session_id = uuid.uuid4().hex
            payload = self._build_payload()
        await self._publish_state("Manual broadcast", payload)


def summary_line(
    label: str, value: str, is_bold: bool = False, is_red: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-gray-500 font-medium"),
        rx.el.span(
            value,
            class_name=rx.cond(
                is_bold,
                rx.cond(is_red, "font-bold text-red-500", "font-bold text-gray-900"),
                "text-gray-700 font-medium",
            ),
        ),
        class_name="flex justify-between items-center py-2",
    )


def status_pill() -> rx.Component:
    return rx.el.span(
        ExampleFiveState.connection_status,
        class_name=rx.match(
            ExampleFiveState.connection_status,
            ("connected", "px-2 py-1 rounded-full text-xs font-bold bg-green-100 text-green-700"),
            ("connecting", "px-2 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-700"),
            ("error", "px-2 py-1 rounded-full text-xs font-bold bg-red-100 text-red-700"),
            "px-2 py-1 rounded-full text-xs font-bold bg-gray-100 text-gray-500",
        ),
    )


def example_five_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Example 5: Redis Pub/Sub State Sync",
                class_name="text-4xl font-black text-gray-900 mb-2",
            ),
            rx.el.p(
                "Derived state is still computed locally, but state changes are broadcast through Redis so other sessions can react.",
                class_name="text-lg text-gray-600 mb-12",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Configuration",
                        class_name="text-xl font-bold mb-6 flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Select Product",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.foreach(
                                ExampleFiveState.products,
                                lambda p: rx.el.option(p.name, value=p.id.to_string()),
                            ),
                            on_change=ExampleFiveState.select_product,
                            class_name="w-full p-3 rounded-xl border border-gray-200 bg-white focus:ring-2 focus:ring-indigo-500 outline-none appearance-none",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Quantity",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            type="number",
                            on_change=ExampleFiveState.change_quantity,
                            class_name="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none",
                            default_value=ExampleFiveState.quantity.to_string(),
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Discount Code",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            placeholder="Try REFLEX20 or DEVMODE",
                            on_change=ExampleFiveState.update_discount_code.debounce(300),
                            class_name="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none",
                        ),
                        rx.cond(
                            ExampleFiveState.discount_percent > 0,
                            rx.el.p(
                                f"Applied {ExampleFiveState.discount_percent * 100:.0f}% discount!",
                                class_name="text-xs text-green-600 font-bold mt-2",
                            ),
                            None,
                        ),
                        class_name="mb-2",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Broadcast State",
                            on_click=ExampleFiveState.broadcast_state,
                            class_name="w-full px-4 py-3 bg-indigo-600 text-white rounded-xl text-sm font-bold hover:bg-indigo-700 transition-colors",
                        ),
                        class_name="mt-6",
                    ),
                    class_name="p-8 bg-white border border-gray-100 rounded-3xl shadow-sm h-full",
                ),
                class_name="lg:col-span-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Derived Pricing Engine",
                        class_name="text-xl font-bold mb-6",
                    ),
                    rx.el.div(
                        rx.icon(
                            ExampleFiveState.selected_product.icon,
                            class_name="h-5 w-5 text-indigo-600",
                        ),
                        rx.el.p(
                            ExampleFiveState.selected_product.name,
                            class_name="font-semibold text-gray-800",
                        ),
                        class_name="flex items-center gap-2 mb-4",
                    ),
                    rx.el.div(
                        summary_line(
                            "Unit Price",
                            f"${ExampleFiveState.selected_product.price:.2f}",
                        ),
                        summary_line("Subtotal", f"${ExampleFiveState.subtotal:.2f}"),
                        rx.cond(
                            ExampleFiveState.discount_amount > 0,
                            summary_line(
                                "Discount",
                                f"-${ExampleFiveState.discount_amount:.2f}",
                                is_red=True,
                            ),
                            None,
                        ),
                        summary_line(
                            "Tax (8.25%)", f"${ExampleFiveState.tax_amount:.2f}"
                        ),
                        rx.el.div(class_name="my-4 border-t border-gray-100"),
                        summary_line(
                            "Total Amount",
                            f"${ExampleFiveState.total:.2f}",
                            is_bold=True,
                        ),
                        class_name="bg-gray-50 p-6 rounded-2xl",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Redis Pub/Sub",
                            class_name="text-[10px] font-black text-gray-400 mb-4 tracking-widest",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span("Status", class_name="text-xs text-gray-500"),
                                status_pill(),
                                class_name="flex items-center gap-2",
                            ),
                            rx.el.p(
                                "URL: configured via REDIS_URL",
                                class_name="text-xs text-gray-500",
                            ),
                            rx.el.p(
                                f"Channel: {REDIS_CHANNEL}",
                                class_name="text-xs text-gray-500",
                            ),
                            rx.el.p(
                                ExampleFiveState.last_message,
                                class_name="text-xs text-indigo-600 font-semibold",
                            ),
                            class_name="space-y-2",
                        ),
                        rx.el.button(
                            "Reconnect Listener",
                            on_click=ExampleFiveState.listen_redis,
                            disabled=ExampleFiveState.is_listening,
                            class_name="mt-4 w-full px-4 py-2 bg-gray-100 text-gray-600 rounded-xl text-sm font-bold hover:bg-gray-200 disabled:opacity-60",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Event Log",
                                class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    ExampleFiveState.event_log,
                                    lambda item: rx.el.p(
                                        item,
                                        class_name="text-xs text-gray-600 mb-1",
                                    ),
                                ),
                                class_name="bg-white border border-gray-100 rounded-xl p-4",
                            ),
                            rx.cond(
                                ExampleFiveState.event_log.length() == 0,
                                rx.el.p(
                                    "No activity yet.",
                                    class_name="text-xs text-gray-400 mt-2",
                                ),
                                None,
                            ),
                            class_name="mt-6",
                        ),
                        class_name="mt-8 border-t border-gray-100 pt-6",
                    ),
                    class_name="p-8 bg-white border border-gray-100 rounded-3xl shadow-sm h-full",
                ),
                class_name="lg:col-span-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-700",
        on_mount=ExampleFiveState.listen_redis,
    )
