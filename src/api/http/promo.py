import json
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.schema import RawPromo
from src.services import PromoService, UserService, TransactionService
from src.schema.transaction import TransactionCause, TransactionType
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/promo",
    tags=["Promo"],
    route_class=DishkaRoute
)


@router.post('/')
async def use_promo(
    raw_promo: RawPromo,
    promo_service: FromDishka[PromoService],
    user_service: FromDishka[UserService],
    transaction_service: FromDishka[TransactionService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    promo = await promo_service.get_one_promo(name=raw_promo.name)
    if not promo:
        return JSONResponse(status_code=404, content='Promo not found')

    user = await user_service.get_one_user(user_id=user_data.user.id)
    if raw_promo.name in user.used_coupons.get('coupons'):
        return JSONResponse(status_code=403, content='User already has used this promo')

    updated_used_coupons = user.used_coupons
    if user.used_coupons:
        updated_used_coupons['coupons'].append(raw_promo.name) 
    else:
        updated_used_coupons['coupons'] = [raw_promo]
        
    await user_service.update_user(user_id=user_data.user.id, used_coupons=json.dumps(updated_used_coupons))
    await transaction_service.add_transaction(
        id=uuid.uuid4(),
        user_id=user_data.user.id,
        type=TransactionType.DEPOSIT,
        cause=TransactionCause.COUPON,
        amount=promo.bonus_amount,
    )

    return JSONResponse(status_code=200, content='success')
