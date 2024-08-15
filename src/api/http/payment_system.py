from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.services import BileeService
from src.api.schema.payment import TopUpSchema
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/payment",
    tags=["Payment System"],
    route_class=DishkaRoute,
)


@router.post('/')
async def top_up(
    data: TopUpSchema,
    bilee_service: FromDishka[BileeService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    response = bilee_service.create_invoice(amount=10, method=data.method.value)

    return JSONResponse(
        status_code=200,
        content=dict(response=response),
    )
