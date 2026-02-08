import reflex as rx
from reflex_state_examples.states.navigation import NavState


def nav_item(label: str, icon: str, route: str) -> rx.Component:
    is_active = NavState.router.page.path == route
    return rx.el.button(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(label, class_name="font-medium"),
        on_click=lambda: NavState.set_active_page(route),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 w-full px-4 py-3 bg-indigo-600 text-white rounded-xl shadow-md transition-all",
            "flex items-center gap-3 w-full px-4 py-3 text-gray-600 hover:bg-indigo-50 hover:text-indigo-600 rounded-xl transition-all",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("layers", class_name="h-8 w-8 text-indigo-600"),
                    class_name="p-2 bg-indigo-100 rounded-lg",
                ),
                rx.el.div(
                    rx.el.h2(
                        "ReflexState", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Concept Lab",
                        class_name="text-xs text-gray-500 font-medium uppercase tracking-wider",
                    ),
                ),
                class_name="flex items-center gap-3 mb-10 px-2",
            ),
            rx.el.nav(
                rx.el.p(
                    "State Paradigms",
                    class_name="px-4 mb-3 text-xs font-bold text-gray-400 uppercase tracking-widest",
                ),
                rx.el.div(
                    nav_item("In-Memory State", "database", "/in-memory"),
                    nav_item("Derived State", "calculator", "/derived"),
                    nav_item("Backend Sync", "refresh-cw", "/sync"),
                    nav_item("Transactional", "shield-check", "/transactional"),
                    class_name="flex flex-col gap-2",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/notionists/svg?seed=dev",
                        class_name="h-10 w-10 rounded-full bg-indigo-50",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Reflex Developer",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "v0.8.24", class_name="text-xs text-green-500 font-medium"
                        ),
                    ),
                    class_name="flex items-center gap-3 p-4 bg-gray-50 rounded-2xl border border-gray-100",
                ),
                class_name="mt-auto",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-72 h-screen border-r border-gray-200 p-6 bg-white hidden lg:flex shrink-0 sticky top-0",
    )