import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.services import BileeService, TransactionService, UserService
from src.api.schema.payment import TopUpSchema
from src.api.dependencies import user_provider
from src.schema.transaction import TransactionCause, TransactionType
from src.api.http.exceptions import InvalidPaymentError


router = APIRouter(
    prefix="/payment",
    tags=["Payment System"],
    route_class=DishkaRoute,
)

 
@router.post('/')
async def top_up(
    data: TopUpSchema,
    bilee_service: FromDishka[BileeService],
    transaction_service: FromDishka[TransactionService],
    user_data: WebAppInitData = Depends(user_provider),
) -> dict:
    response = bilee_service.create_invoice(amount=data.amount, method=data.method.value)

    if response.get('success') is True:
        payment_data = response['payment']
        payment_data['url'] = response['url']
        await transaction_service.add_transaction(
            id=payment_data['uuid'],
            user_id=user_data.user.id,
            type=TransactionType.DEPOSIT,
            cause=TransactionCause.DONATE,
            amount=payment_data['amount'],
            payment_data=payment_data
        )

    return response

@router.post("/webhook", response_class=JSONResponse)
async def receive_payment(
    request: Request,
    bilee_service: FromDishka[BileeService],
    transaction_service: FromDishka[TransactionService],
    user_service: FromDishka[UserService],
) -> JSONResponse:
    try:
        payload = await request.json()
        signature = request.headers.get('X-Bilee-Signature')
        payment_id = payload.get('uuid')
        if not payment_id:
            return JSONResponse(status_code=400, content={"error": "Missing payment ID"})

        payment = await transaction_service.get_one_transaction(id=payment_id)
        if not payment:
            return JSONResponse(status_code=400, content={"error": "Payment not found"})
        
        # is_valid = bilee_service.validate_payment(signature, payment.payment_data)
        # if not is_valid:
        #     return JSONResponse(status_code=400, content={"error": "Invalid signature"})


        user = await user_service.get_one_user(user_id=payment.user_id)
        top_up_amount = payload.get('amount')
        await user_service.update_user(user_id=user.user_id, balance=user.balance + top_up_amount)

        if user.referral_id:
            referral = await user_service.get_one_user(user_id=user.referral_id)
            reff_top_up_amount = round(top_up_amount * 0.02, 2)
            await user_service.update_user(user_id=user.referral_id, balance=referral.balance + reff_top_up_amount)
            await transaction_service.add_transaction(
                id=uuid.uuid4(),
                user_id=referral.user_id,
                type=TransactionType.DEPOSIT,
                cause=TransactionCause.REFERRAL,
                amount=reff_top_up_amount,
            )

        return JSONResponse(status_code=200, content={"success": True})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})