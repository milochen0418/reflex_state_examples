import reflex as rx
import asyncio
import random
from faker import Faker

fake = Faker()


class User(rx.Base):
    id: int
    name: str
    email: str
    role: str


class ExampleThreeState(rx.State):
    """Simulated Backend Sync demonstration."""

    users: list[User] = []
    is_loading: bool = False
    error_message: str = ""

    @rx.event(background=True)
    async def fetch_users(self):
        async with self:
            self.is_loading = True
            self.error_message = ""
        await asyncio.sleep(1.5)
        async with self:
            if random.random() < 0.2:
                self.error_message = (
                    "Failed to establish connection to database cluster."
                )
                self.is_loading = False
                return
            new_users = [
                User(
                    id=i,
                    name=fake.name(),
                    email=fake.email(),
                    role=random.choice(["Admin", "Editor", "Viewer"]),
                )
                for i in range(1, 6)
            ]
            self.users = new_users
            self.is_loading = False

    @rx.event(background=True)
    async def delete_user(self, user_id: int):
        async with self:
            self.users = [u for u in self.users if u.id != user_id]
        await asyncio.sleep(0.8)