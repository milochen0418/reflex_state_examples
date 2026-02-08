import reflex as rx
from reflex_state_examples.states.example_one import ExampleOneState


def concept_card(
    title: str, description: str, content: rx.Component, icon: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-5 w-5 text-indigo-600"),
                class_name="p-2 bg-indigo-50 rounded-lg",
            ),
            rx.el.div(
                rx.el.h3(title, class_name="text-lg font-bold text-gray-900"),
                rx.el.p(description, class_name="text-sm text-gray-500"),
            ),
            class_name="flex items-center gap-4 mb-6",
        ),
        content,
        class_name="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def example_one_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Example 1: Pure In-Memory State",
                class_name="text-4xl font-black text-gray-900 mb-2 tracking-tight",
            ),
            rx.el.p(
                "In-memory state lives in the Python Backend State class and is synchronized automatically with the UI via Reflex's websocket connection.",
                class_name="text-lg text-gray-600 max-w-2xl",
            ),
            class_name="mb-12",
        ),
        rx.el.div(
            rx.el.div(
                concept_card(
                    "Numeric State",
                    "A simple integer variable modified by event handlers.",
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Current Value",
                                class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1",
                            ),
                            rx.el.p(
                                ExampleOneState.count.to_string(),
                                class_name="text-5xl font-black text-indigo-600 tabular-nums",
                            ),
                            class_name="text-center py-6 bg-indigo-50/50 rounded-2xl mb-6",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("minus", class_name="h-5 w-5"),
                                on_click=ExampleOneState.decrement,
                                class_name="flex-1 flex justify-center py-3 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors shadow-sm",
                            ),
                            rx.el.button(
                                rx.icon("plus", class_name="h-5 w-5"),
                                on_click=ExampleOneState.increment,
                                class_name="flex-1 flex justify-center py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors shadow-sm",
                            ),
                            class_name="flex gap-3",
                        ),
                        class_name="w-full",
                    ),
                    "hash",
                ),
                concept_card(
                    "Boolean State",
                    "Switching states between True and False for UI logic.",
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "System Active",
                                    class_name="font-semibold text-gray-700",
                                ),
                                rx.el.button(
                                    rx.el.div(
                                        class_name=rx.cond(
                                            ExampleOneState.is_active,
                                            "h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-6 transition-transform",
                                            "h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-1 transition-transform",
                                        )
                                    ),
                                    on_click=ExampleOneState.toggle_active,
                                    class_name=rx.cond(
                                        ExampleOneState.is_active,
                                        "w-12 h-7 bg-green-500 rounded-full transition-colors flex items-center",
                                        "w-12 h-7 bg-gray-200 rounded-full transition-colors flex items-center",
                                    ),
                                ),
                                class_name="flex justify-between items-center p-4 bg-gray-50 rounded-xl mb-3",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Premium Tier",
                                    class_name="font-semibold text-gray-700",
                                ),
                                rx.el.button(
                                    rx.el.div(
                                        class_name=rx.cond(
                                            ExampleOneState.is_premium,
                                            "h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-6 transition-transform",
                                            "h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-1 transition-transform",
                                        )
                                    ),
                                    on_click=ExampleOneState.toggle_premium,
                                    class_name=rx.cond(
                                        ExampleOneState.is_premium,
                                        "w-12 h-7 bg-indigo-500 rounded-full transition-colors flex items-center",
                                        "w-12 h-7 bg-gray-200 rounded-full transition-colors flex items-center",
                                    ),
                                ),
                                class_name="flex justify-between items-center p-4 bg-gray-50 rounded-xl",
                            ),
                        ),
                        rx.el.div(
                            rx.cond(
                                ExampleOneState.is_premium,
                                rx.el.div(
                                    rx.icon(
                                        "sparkles", class_name="h-4 w-4 text-indigo-600"
                                    ),
                                    rx.el.span(
                                        "Premium Features Unlocked",
                                        class_name="text-xs font-bold",
                                    ),
                                    class_name="mt-4 flex items-center gap-2 justify-center py-2 bg-indigo-50 text-indigo-700 rounded-lg animate-pulse",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Standard User",
                                        class_name="text-xs font-bold text-gray-400",
                                    ),
                                    class_name="mt-4 text-center",
                                ),
                            )
                        ),
                    ),
                    "toggle-right",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8",
            ),
            concept_card(
                "Event Lifecycle Visualization",
                "Observe how UI interactions trigger backend handlers which emit state updates back to the frontend.",
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "mouse-pointer-2",
                                    class_name="h-6 w-6 text-indigo-400",
                                ),
                                rx.el.p(
                                    "User Interaction", class_name="text-xs font-bold"
                                ),
                                class_name="flex flex-col items-center gap-2 p-4 border-2 border-dashed border-gray-100 rounded-2xl bg-white",
                            ),
                            rx.icon("arrow-right", class_name="text-gray-300"),
                            rx.el.div(
                                rx.icon("cpu", class_name="h-6 w-6 text-indigo-600"),
                                rx.el.p(
                                    "State.handler()", class_name="text-xs font-bold"
                                ),
                                class_name="flex flex-col items-center gap-2 p-4 border-2 border-indigo-100 rounded-2xl bg-indigo-50/30",
                            ),
                            rx.icon("arrow-right", class_name="text-gray-300"),
                            rx.el.div(
                                rx.icon(
                                    "refresh-cw", class_name="h-6 w-6 text-green-500"
                                ),
                                rx.el.p(
                                    "UI Re-render",
                                    class_name="text-xs font-bold text-green-600",
                                ),
                                class_name="flex flex-col items-center gap-2 p-4 border-2 border-green-100 rounded-2xl bg-green-50/30",
                            ),
                            class_name="flex items-center justify-between px-4 mb-8",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Event Stream (Backend Log)",
                                    class_name="text-xs font-bold text-white mb-2 uppercase tracking-widest",
                                ),
                                rx.el.div(
                                    rx.foreach(
                                        ExampleOneState.event_log,
                                        lambda log: rx.el.p(
                                            f"> {log}",
                                            class_name="font-mono text-sm text-green-400 mb-1",
                                        ),
                                    ),
                                    class_name="bg-gray-900 p-6 rounded-xl shadow-inner min-h-[160px]",
                                ),
                                class_name="flex-1",
                            ),
                            class_name="w-full",
                        ),
                        class_name="w-full",
                    )
                ),
                "activity",
            ),
        ),
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-700",
    )