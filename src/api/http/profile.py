import uuid
from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.schema import User, Order, Transaction
from src.services import UserService, OrderService, TransactionService


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    route_class=DishkaRoute
)


@router.get("/", response_model=User)
async def get_user(user_id: int, user_service: FromDishka[UserService]) -> JSONResponse:
    user = await user_service.get_user(user_id=user_id)
    if user:
        return JSONResponse(
            status_code=200,
            content=dict(user=user),
        )
    
    return JSONResponse(
        status_code=404,
        content='User not found.',
    )


@router.get("/orders", response_model=List[Order])
async def get_user_orders(
    user_id: int, order_service: FromDishka[OrderService]
) -> JSONResponse:
    orders = await order_service.get_orders(user_id=user_id)
    if orders:
        return JSONResponse(
            status_code=200,
            content=dict(orders=orders)
        )
    
    return JSONResponse(
        status_code=404,
        content=dict('User has no orders.')
    )


@router.get("/orders/{order_id}", response_model=List[Order])
async def get_one_order(
    order_id: uuid.UUID,
    order_service: FromDishka[OrderService]
) -> JSONResponse:
    order = await order_service.get_one_order(order_id=order_id)
    if order:
        return JSONResponse(
            status_code=200,
            content=dict(order=order)
        )
    
    return JSONResponse(
        status_code=404,
        content=dict('Order not found')
    )


@router.get("/transactions", response_model=List[Transaction])
async def get_user_transactions(
    user_id: int, transaction_service: FromDishka[TransactionService]
) -> JSONResponse:
    transactions = await transaction_service.get_transactions(user_id=user_id)
    if transactions:
        return JSONResponse(
            status_code=200,
            content=dict(transactions=transactions)
        )
    
    return JSONResponse(
        status_code=404,
        content=dict('User has no transactions')
    )


@router.get("/transactions/{transaction_id}", response_model=List[Transaction])
async def get_one_transaction(
    transaction_id: uuid.UUID,
    transaction_service: FromDishka[TransactionService]
) -> JSONResponse:
    transactions = await transaction_service.get_one_transaction(id=transaction_id)
    if transactions:
        return JSONResponse(
            status_code=200,
            content=dict(transactions=transactions)
        )
    
    return JSONResponse(
        status_code=404,
        content=dict('Transaction not found')
    )
