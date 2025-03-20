import uuid
from typing import TypeVar, Type, Generic, Optional, List, Dict, Literal, Union
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from rb_commons.http.exceptions import NotFoundException
from rb_commons.orm.exceptions import DatabaseException, InternalException

ModelType = TypeVar('ModelType', bound=declarative_base())

class BaseManager(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.data = None
        self.filters = {}

    async def get(self, pk: Union[str, int, uuid.UUID]) -> Optional[ModelType]:
        """
           get object based on conditions
       """
        query = select(self.model).filter_by(id=pk)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise NotFoundException(
                message="Object does not exist",
                status=404,
                code="0001",
            )

        return instance

    def filter(self, **kwargs) -> 'BaseManager[ModelType]':
        """
           Filter objects based on conditions
       """
        self.filters.update(kwargs)
        return self

    async def all(self) -> List[ModelType]:
        """Return all filtered results."""
        query = select(self.model).filter_by(**self.filters)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def first(self) -> Optional[ModelType]:
        """Return the first matching object, or None."""
        query = select(self.model).filter_by(**self.filters)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def count(self) -> int:
        """Return the count of matching records."""
        query = select(self.model).filter_by(**self.filters)
        result = await self.session.execute(query)
        return len(result.scalars().all())

    async def create(self, **kwargs) -> ModelType:
        """
               Create a new object
        """
        obj = self.model(**kwargs)

        try:
            self.session.add(obj)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.session.rollback()
            raise DatabaseException(f"Constraint violation: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Database error occurred: {str(e)}") from e
        except Exception as e:
            await self.session.rollback()
            raise InternalException(f"Unexpected error during creation: {str(e)}") from e


    async def delete(self, id: Optional[int] = None, **filters):
        """
        Delete object(s) with flexible filtering options

        :param id: Specific ID to delete
        :param filters: Additional filter conditions
        :return: Number of deleted records or None
        """
        try:
            if id is not None:
                filters['id'] = id

            delete_stmt = delete(self.model).filter_by(**filters)
            result = await self.session.execute(delete_stmt)
            await self.session.commit()
            return result
        except NoResultFound:
            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Delete operation failed: {str(e)}") from e

    async def bulk_delete(self, **filters) -> int:
        """
        Bulk delete with flexible filtering

        :param filters: Conditions for bulk deletion
        :return: Number of deleted records
        """
        try:
            delete_stmt = delete(self.model).filter_by(**filters)
            result = await self.session.execute(delete_stmt)
            await self.session.commit()
            return result.rowcount()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Bulk delete failed: {str(e)}") from e

    async def update_by_filters(self, filters: Dict, **update_fields) -> Optional[ModelType]:
        """
        Update object(s) with flexible filtering options

        :param filters: Conditions for selecting records to update
        :param update_fields: Fields and values to update
        :return: Number of updated records
        """
        if not update_fields:
            raise InternalException("No fields provided for update")

        try:
            update_stmt = update(self.model).filter_by(**filters).values(**update_fields)
            await self.session.execute(update_stmt)
            await self.session.commit()
            updated_instance = await self.get(**filters)
            return updated_instance
        except IntegrityError as e:
            await self.session.rollback()
            raise InternalException(f"Constraint violation: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Update operation failed: {str(e)}") from e

    async def update(self, instance: ModelType, **update_fields) -> Optional[ModelType]:
        """
        Update an existing database instance with new fields

        :param instance: The database model instance to update
        :param update_fields: Keyword arguments of fields to update
        :return: The updated instance

        :raises ValueError: If no update fields are provided
        :raises RuntimeError: For database-related errors
        """
        # Validate update fields
        if not update_fields:
            raise InternalException("No fields provided for update")

        try:
            # Apply updates directly to the instance
            for key, value in update_fields.items():
                setattr(instance, key, value)

            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)

            return instance

        except IntegrityError as e:
            await self.session.rollback()
            raise InternalException(f"Constraint violation: {str(e)}") from e

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Update operation failed: {str(e)}") from e

    async def save(self, instance: ModelType) -> Optional[ModelType]:
        """
        Save instance

        :param instance: The database model instance to save
        :return: The saved instance

        :raises ValueError: If no update fields are provided
        :raises RuntimeError: For database-related errors
        """
        try:
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance

        except IntegrityError as e:
            await self.session.rollback()
            raise InternalException(f"Constraint violation: {str(e)}") from e

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Update operation failed: {str(e)}") from e


    async def is_exists(self, **kwargs) -> bool:
        return await self.get(**kwargs) is not None

