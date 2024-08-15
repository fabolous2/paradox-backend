from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.services import UserService
from src.api.schema.referral import ReferralCode, NewReferralCode
from src.main.config import settings
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/referral",
    tags=["Referral System"],
    route_class=DishkaRoute,
)


@router.get("/get_code", response_model=ReferralCode)
async def get_referral_code(
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Union[JSONResponse, ReferralCode]:
    user = await user_service.get_one_user(user_id=user_data.user.id)
    if not user:
        return JSONResponse(status_code=404, content="User not found")
    
    referral_url = settings.get_referral_url(user.referral_code)

    return ReferralCode(code=user.referral_code, referral_url=referral_url)


@router.post("/set_code", response_model=ReferralCode)
async def set_code(
    referral_code: NewReferralCode,
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Union[JSONResponse, ReferralCode]:
    user = await user_service.get_one_user(user_id=user_data.user.id)
    if not user:
        return JSONResponse(status_code=404, content=dict(description='User not found'))
    elif user.referral_code == referral_code:
        return JSONResponse(status_code=400, content=dict(description='This referral code already in use by user.'))
    
    try:
        await user_service.update_user(user_id=user_data.user.id, referral_code=referral_code)
        referral_url = settings.get_referral_url(referral_code)

        return ReferralCode(code=user.referral_code, referral_url=referral_url)
    except Exception as ex:
        print(ex)
        return JSONResponse(status_code=400, content=dict(detail='Probably this referral code is already taken'))
