import asyncio
import os

from app.core.db import sessionmanager
from app.modules.users.service import get_user_by_email, create_user


async def main():
    sessionmanager.init_db()
    email = os.getenv("SEED_SUPERADMIN_EMAIL", "admin@example.com")
    password = os.getenv("SEED_SUPERADMIN_PASSWORD", "admin123")
    full_name = os.getenv("SEED_SUPERADMIN_NAME", "Super Admin")
    async with sessionmanager.session_factory() as session:  # type: ignore
        existing = await get_user_by_email(session, email)
        if existing:
            if existing.role != "superadmin":
                existing.role = "superadmin"
                await session.commit()
            print("Superadmin already exists:", email)
            return
        await create_user(
            session,
            email=email,
            password=password,
            full_name=full_name,
            role="superadmin",
        )
        print("Superadmin created:", email)


if __name__ == "__main__":
    asyncio.run(main())
