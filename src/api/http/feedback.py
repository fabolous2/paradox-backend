import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependency_injector.wiring import inject, Provide

from aiogram.utils.web_app import WebAppInitData

from src.services import FeedbackService, UserService
from src.api.schema.feedback import CreateFeedback
from src.schema import Feedback
from src.api.dependencies import user_provider
from src.api.http.consts import ADMINS
from src.api.http.exceptions import MethodNotAllowedError
from src.schema import User
from src.main.ioc import Container


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post("/post", response_class=JSONResponse)
@inject
async def post_feedback(
    data: CreateFeedback,
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    await feedback_service.add_feedback(
        id=uuid.uuid4(),
        product_id=data.product.id,
        order_id=data.order_id,
        user_id=user_data.user.id,
        text=data.text,
        stars=data.stars,
        time=datetime.now()
    )
    

    return JSONResponse(
        status_code=200,
        content=dict(detail='success')
    )


@router.get("/", response_model=List[Feedback])
@inject
async def get_feedbacks(
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
) -> List[Feedback]:
    response = await feedback_service.get_feedbacks(is_active=True)
    return response


@router.get("/{feedback_id}", response_model=Feedback)
@inject
async def get_one_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
) -> Feedback:
    return await feedback_service.get_one_feedback(id=feedback_id)


@router.get("/is_user_posted_feedback/{order_id}")
@inject
async def is_user_posted_feedback(
    order_id: uuid.UUID,
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Feedback:
    return await feedback_service.get_one_feedback(user_id=user_data.user.id, order_id=order_id)


@router.get("/remove/{feedback_id}", response_class=JSONResponse)
@inject
async def remove_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    if not user_data.user.id in ADMINS:
        raise MethodNotAllowedError

    await feedback_service.delete_feedback(feedback_id=feedback_id)

    return JSONResponse(
        status_code=200,
        content=dict(detail='success')
    )


@router.get("/user/{user_id}", response_model=User)
@inject
async def get_user_feedbacks(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    return await user_service.get_one_user(user_id=user_id)
