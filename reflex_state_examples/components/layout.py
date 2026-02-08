import reflex as rx
from reflex_state_examples.components.sidebar import sidebar


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(content, class_name="max-w-5xl mx-auto w-full"),
            class_name="flex-1 min-h-screen bg-gray-50 p-4 md:p-8 lg:p-12 overflow-y-auto",
        ),
        class_name="flex min-h-screen font-['Inter'] text-gray-900",
    )