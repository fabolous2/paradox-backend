from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.main.config import settings

from src.services import (
    UserService,
    ProductService,
    TransactionService,
    OrderService,
    PromoService,
    SupercellAuthService,
    FeedbackService,
    BileeService,
)
from src.data.dal import (
    UserDAL,
    ProductDAL,
    TransactionDAL,
    OrderDAL,
    PromoDAL,
    FeedbackDAL
)


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP, provides=AsyncEngine)
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(url=settings.db_connection_url)

    @provide(scope=Scope.APP, provides=async_sessionmaker[AsyncSession])
    def get_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_async_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            yield session


class DALProvider(Provider):
    user_dal = provide(UserDAL, scope=Scope.REQUEST, provides=UserDAL)
    product_dal = provide(ProductDAL, scope=Scope.REQUEST, provides=ProductDAL)
    transaction_dal = provide(TransactionDAL, scope=Scope.REQUEST, provides=TransactionDAL)
    order_dal = provide(OrderDAL, scope=Scope.REQUEST, provides=OrderDAL)
    promo_dal = provide(PromoDAL, scope=Scope.REQUEST, provides=PromoDAL)
    feedback_dal = provide(FeedbackDAL, scope=Scope.REQUEST, provides=FeedbackDAL)


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)
    product_service = provide(ProductService, scope=Scope.REQUEST, provides=ProductService)
    transaction_service = provide(TransactionService, scope=Scope.REQUEST, provides=TransactionService)
    order_service = provide(OrderService, scope=Scope.REQUEST, provides=OrderService)
    promo_service = provide(PromoService, scope=Scope.REQUEST, provides=PromoService)
    supercell_service = provide(SupercellAuthService, scope=Scope.REQUEST, provides=SupercellAuthService)
    feedback_service = provide(FeedbackService, scope=Scope.REQUEST, provides=FeedbackService)
    bilee_service = provide(BileeService, scope=Scope.REQUEST, provides=BileeService)
    