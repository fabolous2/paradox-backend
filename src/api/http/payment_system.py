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


@router.post('/')
async def top_up(
    user_id: int,
    summa: RawSumma,
    method: TopUpMethod,
    user_service: FromDishka[UserService],
) -> JSONResponse:
    user = await user_service.get_one_user(user_id=user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=dict(detail='User not found.')
        )
    
