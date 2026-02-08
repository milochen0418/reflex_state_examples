import reflex as rx
from reflex_state_examples.components.layout import layout
from reflex_state_examples.states.example_one import example_one_content
from reflex_state_examples.states.example_two import example_two_content
from reflex_state_examples.states.example_three import example_three_content
from reflex_state_examples.states.example_four import example_four_content
from reflex_state_examples.states.example_five import example_five_content
from reflex_state_examples.states.navigation import NavState


def inmemory_page() -> rx.Component:
    return layout(example_one_content())


def index() -> rx.Component:
    return rx.el.div()


def derived_page() -> rx.Component:
    return layout(example_two_content())


def sync_page() -> rx.Component:
    return layout(example_three_content())


def transactional_page() -> rx.Component:
    return layout(example_four_content())


def redis_page() -> rx.Component:
    return layout(example_five_content())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(inmemory_page, route="/in-memory")
app.add_page(index, route="/", on_load=rx.redirect("/in-memory"))
app.add_page(derived_page, route="/derived")
app.add_page(sync_page, route="/sync")
app.add_page(transactional_page, route="/transactional")
app.add_page(redis_page, route="/redis-sync")