from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.services import BileeService
from src.api.schema.payment import TopUpSchema


router = APIRouter(
    prefix="/payment",
    tags=["Payment System"],
    route_class=DishkaRoute
)


@router.post('/')
async def top_up(
    data: TopUpSchema,
    bilee_service: FromDishka[BileeService],
) -> JSONResponse:
    print(data.method.value)
    print(data.amount)
    response = bilee_service.create_invoice(amount=10, method=data.method.value)

    return JSONResponse(status_code=200, content=dict(service_response=response))
