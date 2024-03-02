from typing import Optional

import motor.motor_asyncio

from backend.core.entites import User

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017") # TODO


class UserRepository:
    def __init__(self) -> None:
        self._db = client["database"] # TODO
        self._user_collection = self._db["users"]

    async def save(self, user: User) -> None:
        await self._user_collection.insert_one(user.as_dict)

    async def get_from_email(self, user_email: str) -> Optional[User]:
        user_data = await self._user_collection.find_one({"email": user_email})
        if not user_data:
            return None
        print(user_data, '!')
        return User.from_dict(**user_data)


user_repository = UserRepository()
