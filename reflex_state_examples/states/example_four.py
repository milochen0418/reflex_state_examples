import reflex as rx
import re


class TransactionalUser(rx.Base):
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