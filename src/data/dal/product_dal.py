from typing import Optional, TypeAlias, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import Product
from src.data.models import ProductModel


_ProductResult: TypeAlias = Result[tuple[ProductModel]]


class ProductDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(ProductModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, user_id: int, **kwargs) -> None:
        query = update(ProductModel).where(ProductModel.user_id == user_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(ProductModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(ProductModel, key)
                    )
                )
            )
        query = select(exists(ProductModel))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, user_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(user_id=user_id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(ProductModel, column_name)
                for column_name in column_names
                if hasattr(ProductModel, column_name)
            )
        ).where(ProductModel.user_id == user_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_ProductResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        if kwargs:
            query = select(ProductModel).filter_by(**kwargs)
        query = select(ProductModel)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Product]:
        res = await self._get(**kwargs)

        if res:
            db_product = res.scalar_one_or_none()
            return Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                price=db_product.price,
                instruction=db_product.instruction,
                purchase_count=db_product.purchase_count,
            )

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Product]]:
        res = await self._get(**kwargs)

        if res:
            db_products = res.scalars().all()
            return [
                Product(
                    id=db_product.id,
                    name=db_product.name,
                    description=db_product.description,
                    price=db_product.price,
                    instruction=db_product.instruction,
                    purchase_count=db_product.purchase_count,
            )
                for db_product in db_products
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(ProductModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
