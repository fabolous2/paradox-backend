import uuid
import json
from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.schema import User, Order, Transaction
from src.services import UserService, OrderService, TransactionService
from src.api.dependencies import user_provider
from src.api.schema.order import CreateOrderDTO
from src.schema.order import OrderStatus


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    route_class=DishkaRoute,
)


@router.get("/", response_model=User)
async def get_user(
    user_service: FromDishka[UserService],
    # user_data: WebAppInitData = Depends(user_provider),
) -> Optional[User]:
    user = await user_service.get_one_user(user_id=6384960822)

    return user
    
    
@router.get("/orders", response_model=List[Order])
async def get_user_orders(
    order_service: FromDishka[OrderService],
    # user_data: WebAppInitData = Depends(user_provider),
) -> Optional[List[Order]]:
    orders = await order_service.get_orders(user_id=6384960822)

    return orders


@router.get("/orders/{order_id}", response_model=Order)
async def get_one_order(
    order_id: uuid.UUID,
    order_service: FromDishka[OrderService],
    # user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Order]:
    order = await order_service.get_one_order(
        # user_id=6384960822,
        id=order_id,
    )
    return order
   

@router.get("/transactions", response_model=List[Transaction])
async def get_user_transactions(
    transaction_service: FromDishka[TransactionService],
    # user_data: WebAppInitData = Depends(user_provider),
) -> Optional[List[Transaction]]:
    transactions = await transaction_service.get_transactions(user_id=6384960822, is_successful=True)
    return transactions


@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_one_transaction(
    transaction_id: uuid.UUID,
    transaction_service: FromDishka[TransactionService],
    # user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Transaction]:
    transaction = await transaction_service.get_one_transaction(
        # user_id=user_data.user.id,
        id=transaction_id,
    )
    print(transaction)
    return transaction


@router.post("/orders")
async def create_order(
    order_data: CreateOrderDTO,
    order_service: FromDishka[OrderService],
    # user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    order = await order_service.add_order(
        id=uuid.uuid4(),
        user_id=6384960822,
        product_id=order_data.product_id,
        status=OrderStatus.PROGRESS,
        additional_data=order_data.additional_data.model_json_schema(),
        name="some name",
        price=100,
    )
    
    return JSONResponse(status_code=201, content={"message": "Order created"})