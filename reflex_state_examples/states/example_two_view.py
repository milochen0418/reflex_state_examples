import reflex as rx
from reflex_state_examples.states.example_two import ExampleTwoState


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


def example_two_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Example 2: Derived State",
                class_name="text-4xl font-black text-gray-900 mb-2",
            ),
            rx.el.p(
                "Derived state (@rx.var) calculates values automatically on the backend whenever their source dependencies change.",
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
                                ExampleTwoState.products,
                                lambda p: rx.el.option(p.name, value=p.id.to_string()),
                            ),
                            on_change=ExampleTwoState.select_product,
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
                            on_change=ExampleTwoState.change_quantity,
                            class_name="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none",
                            default_value=ExampleTwoState.quantity.to_string(),
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
                            on_change=ExampleTwoState.set_discount_code.debounce(300),
                            class_name="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none",
                        ),
                        rx.cond(
                            ExampleTwoState.discount_percent > 0,
                            rx.el.p(
                                f"Applied {ExampleTwoState.discount_percent * 100:.0f}% discount!",
                                class_name="text-xs text-green-600 font-bold mt-2",
                            ),
                            None,
                        ),
                        class_name="mb-2",
                    ),
                    class_name="p-8 bg-white border border-gray-100 rounded-3xl shadow-sm h-full",
                ),
                class_name="lg:col-span-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Derived Pricing Engine", class_name="text-xl font-bold mb-6"
                    ),
                    rx.el.div(
                        summary_line(
                            "Unit Price",
                            f"${ExampleTwoState.selected_product.price:.2f}",
                        ),
                        summary_line("Subtotal", f"${ExampleTwoState.subtotal:.2f}"),
                        rx.cond(
                            ExampleTwoState.discount_amount > 0,
                            summary_line(
                                "Discount",
                                f"-${ExampleTwoState.discount_amount:.2f}",
                                is_red=True,
                            ),
                            None,
                        ),
                        summary_line(
                            "Tax (8.25%)", f"${ExampleTwoState.tax_amount:.2f}"
                        ),
                        rx.el.div(class_name="my-4 border-t border-gray-100"),
                        summary_line(
                            "Total Amount",
                            f"${ExampleTwoState.total:.2f}",
                            is_bold=True,
                        ),
                        class_name="bg-gray-50 p-6 rounded-2xl",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "RE-CALCULATION FLOW",
                            class_name="text-[10px] font-black text-gray-400 mb-4 tracking-widest",
                        ),
                        rx.el.div(
                            rx.el.div(
                                "Sources",
                                class_name="bg-indigo-100 text-indigo-700 px-2 py-1 rounded text-[10px] font-bold",
                            ),
                            rx.icon("arrow-right", class_name="h-3 w-3 text-gray-300"),
                            rx.el.div(
                                "@rx.var Engine",
                                class_name="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] font-bold",
                            ),
                            rx.icon("arrow-right", class_name="h-3 w-3 text-gray-300"),
                            rx.el.div(
                                "Reactive UI",
                                class_name="bg-blue-100 text-blue-700 px-2 py-1 rounded text-[10px] font-bold",
                            ),
                            class_name="flex items-center justify-between",
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
    )