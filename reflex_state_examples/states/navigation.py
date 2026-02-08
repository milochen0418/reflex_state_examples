import reflex as rx


class NavState(rx.State):
    """Handles sidebar navigation and active page highlighting."""

    active_page: str = "/in-memory"

    @rx.event
    def set_active_page(self, route: str):
        self.active_page = route
        return rx.redirect(route)