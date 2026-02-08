import asyncio
import random

import reflex as rx
from pydantic import BaseModel
from faker import Faker

fake = Faker()


class User(BaseModel):
    id: int
    name: str
    email: str
    role: str


class ExampleThreeState(rx.State):
    """Simulated Backend Sync demonstration."""

    users: list[User] = []
    is_loading: bool = False
    error_message: str = ""

    @rx.event(background=True)
    async def fetch_users(self):
        async with self:
            self.is_loading = True
            self.error_message = ""
        await asyncio.sleep(1.5)
        async with self:
            if random.random() < 0.2:
                self.error_message = (
                    "Failed to establish connection to database cluster."
                )
                self.is_loading = False
                return
            new_users = [
                User(
                    id=i,
                    name=fake.name(),
                    email=fake.email(),
                    role=random.choice(["Admin", "Editor", "Viewer"]),
                )
                for i in range(1, 6)
            ]
            self.users = new_users
            self.is_loading = False

    @rx.event(background=True)
    async def delete_user(self, user_id: int):
        async with self:
            self.users = [u for u in self.users if u.id != user_id]
        await asyncio.sleep(0.8)


def user_row(user: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={user['email']}",
                    class_name="h-8 w-8 rounded-full",
                ),
                rx.el.span(user["name"], class_name="font-medium text-gray-900"),
                class_name="flex items-center gap-3",
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(user["email"], class_name="py-4 px-4 text-gray-500 text-sm"),
        rx.el.td(
            rx.el.span(
                user["role"],
                class_name=rx.match(
                    user["role"],
                    (
                        "Admin",
                        "px-2 py-1 bg-purple-100 text-purple-700 text-xs font-bold rounded-full",
                    ),
                    (
                        "Editor",
                        "px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded-full",
                    ),
                    "px-2 py-1 bg-gray-100 text-gray-700 text-xs font-bold rounded-full",
                ),
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon(
                    "trash-2", class_name="h-4 w-4 text-gray-400 hover:text-red-500"
                ),
                on_click=lambda: ExampleThreeState.delete_user(user["id"]),
                class_name="p-2 rounded-lg hover:bg-red-50 transition-colors",
            ),
            class_name="py-4 px-4 text-right",
        ),
        class_name="border-b border-gray-50 hover:bg-gray-50/50 transition-colors",
    )


def example_three_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Example 3: Backend Sync",
                class_name="text-4xl font-black text-gray-900 mb-2",
            ),
            rx.el.p(
                "Simulating asynchronous API interactions with background tasks and state locking.",
                class_name="text-lg text-gray-600 mb-12",
            ),
        ),
        rx.cond(
            ExampleThreeState.error_message != "",
            rx.el.div(
                rx.el.div(
                    rx.icon("wheat", class_name="h-5 w-5 text-red-600"),
                    rx.el.p(
                        ExampleThreeState.error_message,
                        class_name="font-bold text-red-700",
                    ),
                    rx.el.button(
                        "Retry Connection",
                        on_click=ExampleThreeState.fetch_users,
                        class_name="ml-auto bg-red-600 text-white px-4 py-2 rounded-xl text-sm font-bold shadow-sm hover:bg-red-700 transition-colors",
                    ),
                    class_name="flex items-center gap-4 p-6 bg-red-50 border border-red-100 rounded-3xl mb-8",
                )
            ),
            None,
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Connected User Database", class_name="text-xl font-bold"),
                    rx.el.button(
                        rx.icon(
                            "refresh-cw",
                            class_name=rx.cond(
                                ExampleThreeState.is_loading,
                                "h-4 w-4 animate-spin",
                                "h-4 w-4",
                            ),
                        ),
                        "Sync Data",
                        on_click=ExampleThreeState.fetch_users,
                        disabled=ExampleThreeState.is_loading,
                        class_name="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-xl text-sm font-bold hover:bg-indigo-700 disabled:opacity-50",
                    ),
                    class_name="flex justify-between items-center mb-8 px-2",
                ),
                rx.el.div(
                    rx.cond(
                        ExampleThreeState.is_loading,
                        rx.el.div(
                            rx.foreach(
                                rx.Var.range(5),
                                lambda i: rx.el.div(
                                    class_name="h-12 bg-gray-100 animate-pulse rounded-xl mb-3"
                                ),
                            ),
                            class_name="py-4",
                        ),
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Name",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                    ),
                                    rx.el.th(
                                        "Email",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                    ),
                                    rx.el.th(
                                        "Role",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                    ),
                                    rx.el.th("", class_name="py-3 px-4"),
                                    class_name="border-b border-gray-100",
                                )
                            ),
                            rx.el.tbody(rx.foreach(ExampleThreeState.users, user_row)),
                            class_name="w-full table-auto",
                        ),
                    ),
                    class_name="min-h-[300px]",
                ),
                class_name="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm",
            )
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-700",
        on_mount=ExampleThreeState.fetch_users,
    )