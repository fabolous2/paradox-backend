import uuid
from typing import List, Union, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.schema import User, Order, Transaction
from src.services import UserService, OrderService, TransactionService
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    route_class=DishkaRoute,
)


@router.get("/", response_model=User)
async def get_user(
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[User]:
    user = await user_service.get_one_user(user_id=user_data.user.id)

    return user
    
    
@router.get("/orders", response_model=List[Order])
async def get_user_orders(
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[List[Order]]:
    orders = await order_service.get_orders(user_id=user_data.user.id)
    
    return orders
   

@router.get("/orders/{order_id}", response_model=Order)
async def get_one_order(
    order_id: uuid.UUID,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Order]:
    order = await order_service.get_one_order(
        user_id=user_data.user.id,
        order_id=order_id,
    )
    
    return order
   

@router.get("/transactions", response_model=List[Transaction])
async def get_user_transactions(
    transaction_service: FromDishka[TransactionService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[List[Transaction]]:
    transactions = await transaction_service.get_transactions(user_id=user_data.user.id)

    return transactions


@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_one_transaction(
    transaction_id: uuid.UUID,
    transaction_service: FromDishka[TransactionService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Transaction]:
    transaction = await transaction_service.get_one_transaction(
        user_id=user_data.user.id,
        id=transaction_id,
    )

    return transaction
    