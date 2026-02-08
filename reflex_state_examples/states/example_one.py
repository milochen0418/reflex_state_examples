import reflex as rx


class ExampleOneState(rx.State):
    """Pure In-Memory State demonstration."""

    count: int = 0
    is_active: bool = False
    is_premium: bool = False
    username: str = "DemoUser"
    last_event: str = "None"
    event_log: list[str] = ["Initial state loaded"]

    @rx.event
    def increment(self):
        """Standard event handler to increment count."""
        self.count += 1
        self._log_event(f"Increment: {self.count}")

    @rx.event
    def decrement(self):
        """Standard event handler to decrement count."""
        self.count -= 1
        self._log_event(f"Decrement: {self.count}")

    @rx.event
    def toggle_active(self):
        """Boolean state toggle."""
        self.is_active = not self.is_active
        self._log_event(f"Toggle Active: {self.is_active}")

    @rx.event
    def toggle_premium(self):
        """Boolean state toggle."""
        self.is_premium = not self.is_premium
        self._log_event(f"Toggle Premium: {self.is_premium}")

    def _log_event(self, event_msg: str):
        """Internal helper to update the event log."""
        self.last_event = event_msg
        self.event_log.insert(0, event_msg)
        if len(self.event_log) > 5:
            self.event_log.pop()