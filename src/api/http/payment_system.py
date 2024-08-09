from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.services import UserService
from src.api.schema.referral import ReferralCode, NewReferralCode
from src.main.config import settings
from src.api.schema.payment import RawSumma, TopUpMethod


router = APIRouter(
    prefix="/payment",
    tags=["Payment System"],
    route_class=DishkaRoute
)


@router.get('/')
async def top_up(
    data: TopUpSchema,
    bilee_service: FromDishka[BileeService],
) -> JSONResponse:
    response = bilee_service.create_invoice(amount=data.amount, method=data.method.value)

    return JSONResponse(status_code=200, content=dict(service_response=response))
