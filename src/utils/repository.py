from abc import ABC, abstractmethod
from typing import List
import uuid

from sqlalchemy import delete, insert, select, update


from src.database.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
        return res.scalar_one()

    async def get_all(self, **filters) -> List[dict]:
        async with async_session_maker() as session:
            stmt = select(self.model)
            if filters:
                conditions = [
                    getattr(self.model, key) == value for key, value in filters.items()
                ]
                stmt = stmt.where(*conditions)
            res = await session.execute(stmt)
        return res.scalars().all()

    async def get_one(self, **filters) -> dict:
        res = await self.get(**filters)
        if not res:
            return None
        return res[0]

    async def update(self, id: int | uuid.UUID, **data: dict) -> None:
        data = {key: value for key, value in data.items() if value is not None}

        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )

            res = await session.execute(stmt)
            await session.commit()

            return res.scalar_one_or_none()

    async def delete(self, id: int | uuid.UUID) -> None:
        async with async_session_maker() as session:
            stmt = (
                delete(self.model).where(self.model.id == id).returning(self.model.id)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
