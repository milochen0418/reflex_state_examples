import re

import reflex as rx
from pydantic import BaseModel


class TransactionalUser(BaseModel):
    name: str = "John Doe"
    email: str = "john@example.com"
    theme: str = "light"
    notifications: bool = True


class ExampleFourState(rx.State):
    """Demonstration of Transactional/Complex State Updates."""

    committed_user: TransactionalUser = TransactionalUser()
    draft_name: str = ""
    draft_email: str = ""
    draft_theme: str = "light"
    draft_notifications: bool = True
    current_step: int = 1
    is_committing: bool = False
    show_success_toast: bool = False

    @rx.var
    def name_error(self) -> str:
        if self.current_step == 1 and len(self.draft_name) < 3:
            return "Name must be at least 3 characters."
        return ""

    @rx.var
    def email_error(self) -> str:
        email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        if self.current_step == 1 and (not re.match(email_regex, self.draft_email)):
            return "Invalid email address."
        return ""

    @rx.var
    def is_step_valid(self) -> bool:
        if self.current_step == 1:
            return self.name_error == "" and self.email_error == ""
        return True

    @rx.event
    def start_wizard(self):
        """Initialize draft from committed state (Rollback point)."""
        self.draft_name = self.committed_user.name
        self.draft_email = self.committed_user.email
        self.draft_theme = self.committed_user.theme
        self.draft_notifications = self.committed_user.notifications
        self.current_step = 1

    @rx.event
    def next_step(self):
        if self.is_step_valid:
            self.current_step += 1

    @rx.event
    def prev_step(self):
        self.current_step -= 1

    @rx.event
    def rollback(self):
        """Discard draft and return to step 1 with original values."""
        self.start_wizard()

    @rx.event
    def commit_changes(self):
        """Atomically apply draft to committed state."""
        self.is_committing = True
        self.committed_user = TransactionalUser(
            name=self.draft_name,
            email=self.draft_email,
            theme=self.draft_theme,
            notifications=self.draft_notifications,
        )
        self.is_committing = False
        self.show_success_toast = True
        yield rx.toast("Changes committed successfully!", position="top-center")


def step_indicator(step: int, label: str, current: int) -> rx.Component:
    is_active = current == step
    is_done = current > step
    return rx.el.div(
        rx.el.div(
            rx.cond(
                is_done,
                rx.icon("check", class_name="h-4 w-4 text-white"),
                rx.el.span(
                    step, class_name=rx.cond(is_active, "text-white", "text-gray-400")
                ),
            ),
            class_name=rx.cond(
                is_done,
                "h-8 w-8 rounded-full bg-green-500 flex items-center justify-center",
                rx.cond(
                    is_active,
                    "h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center",
                    "h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center",
                ),
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active,
                "text-xs font-bold text-indigo-600",
                "text-xs font-medium text-gray-400",
            ),
        ),
        class_name="flex flex-col items-center gap-2",
    )


def transactional_flow_diagram() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("arrow_up_to_line", class_name="h-5 w-5 text-orange-500"),
                rx.el.p("Draft Space", class_name="text-[10px] font-bold"),
                class_name="p-3 border border-orange-200 bg-orange-50 rounded-xl flex flex-col items-center gap-1",
            ),
            rx.icon("arrow-right", class_name="text-gray-300 h-4 w-4"),
            rx.el.div(
                rx.icon("shield-check", class_name="h-5 w-5 text-blue-500"),
                rx.el.p("Validation", class_name="text-[10px] font-bold"),
                class_name="p-3 border border-blue-200 bg-blue-50 rounded-xl flex flex-col items-center gap-1",
            ),
            rx.icon("arrow-right", class_name="text-gray-300 h-4 w-4"),
            rx.el.div(
                rx.icon("database", class_name="h-5 w-5 text-green-500"),
                rx.el.p("Commit", class_name="text-[10px] font-bold"),
                class_name="p-3 border border-green-200 bg-green-50 rounded-xl flex flex-col items-center gap-1",
            ),
            class_name="flex items-center gap-4 justify-center py-6",
        ),
        rx.el.p(
            "Changes are held in a secondary 'draft' state until the final validation and commit action is triggered.",
            class_name="text-xs text-center text-gray-500 px-8 pb-4 italic",
        ),
        class_name="bg-white border border-gray-100 rounded-3xl mb-8 shadow-sm",
    )


def step_one() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Full Name", class_name="block text-sm font-bold text-gray-700 mb-2"
            ),
            rx.el.input(
                placeholder="Enter name",
                on_change=ExampleFourState.set_draft_name,
                class_name="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none",
                default_value=ExampleFourState.draft_name,
            ),
            rx.cond(
                ExampleFourState.name_error != "",
                rx.el.p(
                    ExampleFourState.name_error, class_name="text-xs text-red-500 mt-1"
                ),
                None,
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Email Address", class_name="block text-sm font-bold text-gray-700 mb-2"
            ),
            rx.el.input(
                placeholder="Enter email",
                on_change=ExampleFourState.set_draft_email,
                class_name="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none",
                default_value=ExampleFourState.draft_email,
            ),
            rx.cond(
                ExampleFourState.email_error != "",
                rx.el.p(
                    ExampleFourState.email_error, class_name="text-xs text-red-500 mt-1"
                ),
                None,
            ),
        ),
        class_name="animate-in fade-in duration-300",
    )


def step_two() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Preferred Theme",
                class_name="block text-sm font-bold text-gray-700 mb-2",
            ),
            rx.el.select(
                rx.el.option("Light", value="light"),
                rx.el.option("Dark", value="dark"),
                rx.el.option("System", value="system"),
                on_change=ExampleFourState.set_draft_theme,
                value=ExampleFourState.draft_theme,
                class_name="w-full p-3 rounded-xl border border-gray-200 bg-white focus:ring-2 focus:ring-indigo-500 outline-none appearance-none",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Push Notifications", class_name="font-semibold text-gray-700"
                ),
                rx.el.button(
                    rx.el.div(
                        class_name=rx.cond(
                            ExampleFourState.draft_notifications,
                            "h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-6 transition-transform",
                            "h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-1 transition-transform",
                        )
                    ),
                    on_click=ExampleFourState.set_draft_notifications(
                        ~ExampleFourState.draft_notifications
                    ),
                    class_name=rx.cond(
                        ExampleFourState.draft_notifications,
                        "w-12 h-7 bg-indigo-500 rounded-full transition-colors flex items-center",
                        "w-12 h-7 bg-gray-200 rounded-full transition-colors flex items-center",
                    ),
                ),
                class_name="flex justify-between items-center p-4 bg-gray-50 rounded-xl",
            )
        ),
        class_name="animate-in fade-in duration-300",
    )


def step_three() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4("Review Changes", class_name="font-bold text-gray-900 mb-4"),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Name", class_name="text-xs text-gray-400 font-bold uppercase"
                    ),
                    rx.el.p(ExampleFourState.draft_name, class_name="font-medium"),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.span(
                        "Email", class_name="text-xs text-gray-400 font-bold uppercase"
                    ),
                    rx.el.p(ExampleFourState.draft_email, class_name="font-medium"),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.span(
                        "Preferences",
                        class_name="text-xs text-gray-400 font-bold uppercase",
                    ),
                    rx.el.p(
                        f"{ExampleFourState.draft_theme} theme • {rx.cond(ExampleFourState.draft_notifications, 'Notifications On', 'Notifications Off')}",
                        class_name="font-medium",
                    ),
                ),
                class_name="p-6 bg-indigo-50/50 border border-indigo-100 rounded-2xl",
            ),
            class_name="mb-4",
        ),
        class_name="animate-in fade-in duration-300",
    )


def example_four_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Example 4: Transactional Updates",
                class_name="text-4xl font-black text-gray-900 mb-2",
            ),
            rx.el.p(
                "Demonstrating 'Draft vs Commit' patterns for complex multi-step data entry.",
                class_name="text-lg text-gray-600 mb-12",
            ),
        ),
        transactional_flow_diagram(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    step_indicator(1, "Profile", ExampleFourState.current_step),
                    rx.el.div(class_name="h-px w-12 bg-gray-200 mt-4"),
                    step_indicator(2, "Settings", ExampleFourState.current_step),
                    rx.el.div(class_name="h-px w-12 bg-gray-200 mt-4"),
                    step_indicator(3, "Review", ExampleFourState.current_step),
                    class_name="flex items-center gap-4 mb-10 justify-center",
                ),
                rx.match(
                    ExampleFourState.current_step,
                    (1, step_one()),
                    (2, step_two()),
                    (3, step_three()),
                    rx.el.p("Invalid Step"),
                ),
                rx.el.div(
                    rx.el.button(
                        "Discard & Reset",
                        on_click=ExampleFourState.rollback,
                        class_name="px-4 py-2 text-red-600 font-bold text-sm hover:bg-red-50 rounded-xl transition-colors",
                    ),
                    rx.el.div(
                        rx.cond(
                            ExampleFourState.current_step > 1,
                            rx.el.button(
                                "Previous",
                                on_click=ExampleFourState.prev_step,
                                class_name="px-6 py-2 bg-gray-100 text-gray-600 rounded-xl font-bold text-sm hover:bg-gray-200 transition-colors",
                            ),
                            None,
                        ),
                        rx.cond(
                            ExampleFourState.current_step < 3,
                            rx.el.button(
                                "Next Step",
                                on_click=ExampleFourState.next_step,
                                class_name="px-6 py-2 bg-indigo-600 text-white rounded-xl font-bold text-sm hover:bg-indigo-700 transition-colors disabled:opacity-50",
                                disabled=~ExampleFourState.is_step_valid,
                            ),
                            rx.el.button(
                                "Commit All",
                                on_click=[
                                    ExampleFourState.commit_changes,
                                    ExampleFourState.set_current_step(1),
                                ],
                                class_name="px-6 py-2 bg-green-600 text-white rounded-xl font-bold text-sm hover:bg-green-700 transition-colors",
                            ),
                        ),
                        class_name="flex gap-2",
                    ),
                    class_name="flex justify-between items-center mt-12 pt-8 border-t border-gray-100",
                ),
                class_name="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Committed State (Live)",
                    class_name="text-lg font-bold mb-4 flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={ExampleFourState.committed_user.email}",
                            class_name="h-12 w-12 rounded-full bg-white shadow-sm",
                        ),
                        rx.el.div(
                            rx.el.p(
                                ExampleFourState.committed_user.name,
                                class_name="font-black text-gray-900",
                            ),
                            rx.el.p(
                                ExampleFourState.committed_user.email,
                                class_name="text-sm text-gray-500 font-medium",
                            ),
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Active Theme",
                            class_name="text-[10px] font-bold text-gray-400 uppercase tracking-widest",
                        ),
                        rx.el.p(
                            ExampleFourState.committed_user.theme.upper(),
                            class_name="font-bold text-indigo-600 text-sm",
                        ),
                        class_name="mt-4 pt-4 border-t border-gray-100",
                    ),
                    class_name="p-6 bg-gray-50 rounded-3xl border border-gray-200 border-dashed",
                ),
                class_name="mt-8",
            ),
            class_name="max-w-xl mx-auto",
        ),
        on_mount=ExampleFourState.start_wizard,
        class_name="animate-in fade-in slide-in-from-bottom-4 duration-700",
    )