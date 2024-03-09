from typing import Optional, List

import motor.motor_asyncio

from backend.core.entites import User, Store
from backend import settings


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017")  # TODO


class UserRepository:
    def __init__(self) -> None:
        self._db = client[settings.MONGODB_DB_NAME]
        self._user_collection = self._db["user"]

    async def save(self, user: User) -> None:
        await self._user_collection.insert_one(user.as_dict)

    async def get_from_email(self, user_email: str) -> Optional[User]:
        user_data = await self._user_collection.find_one({"email": user_email})
        if not user_data:
            return None

        return User.from_dict(**user_data)

    async def get_from_id(self, id: str) -> Optional[User]:
        user_data = await self._user_collection.find_one({"id": id})
        if not user_data:
            return None

        return User.from_dict(**user_data)

    async def delete(self, user: User) -> None:
        await self._user_collection.delete_one({"id": str(user.id)})

    async def create_indexes(self) -> None:
        await self._user_collection.create_index("email", unique=True)
        await self._user_collection.create_index("id", unique=True)


class StoreRepository:
    def __init__(self) -> None:
        self._db = client[settings.MONGODB_DB_NAME]
        self._store_collection = self._db["store"]

    async def save(self, store: Store) -> None:
        await self._store_collection.insert_one(store.as_dict)

    async def delete(self, store: Store) -> None:
        await self._store_collection.delete_one({"id": str(store.id)})

    async def get_from_id(self, id: str) -> Optional[Store]:
        store_data = await self._store_collection.find_one({"id": id})
        if not store_data:
            return None

        owner_data = store_data.pop("owner")

        return Store.from_dict(owner=User.from_dict(**owner_data), **store_data)

    async def get_all(self) -> List[Store]:
        stores_data = await self._store_collection.find({}).to_list(length=1000)

        return [Store.from_dict(**store_data) for store_data in stores_data]

    async def create_indexes(self) -> None:
        await self._store_collection.create_index("name", unique=True)


user_repository = UserRepository()
store_repository = StoreRepository()
