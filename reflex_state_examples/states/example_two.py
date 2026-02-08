import reflex as rx
import logging


class Product(rx.Base):
    id: int
    name: str
    price: float
    icon: str


class ExampleTwoState(rx.State):
    """Demonstration of Derived State using @rx.var."""

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

    @rx.event
    def change_quantity(self, val: str):
        try:
            self.quantity = max(1, int(val))
        except ValueError as e:
            logging.exception(f"Error: {e}")
            self.quantity = 1

    @rx.event
    def select_product(self, val: str):
        self.selected_product_id = int(val)