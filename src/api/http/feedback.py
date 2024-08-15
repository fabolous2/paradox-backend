import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.services import FeedbackService
from src.api.schema.feedback import CreateFeedback
from src.schema import Feedback
from src.api.dependencies import user_provider
from src.bot.app.main.config import dev_config
from src.api.http.exceptions import MethodNotAllowedError


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    route_class=DishkaRoute,
)


@router.post("/post", response_model=JSONResponse)
async def post_feedback(
    data: CreateFeedback,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    await feedback_service.add_feedback(
        id=uuid.uuid4(),
        product_id=data.product.id,
        user_id=user_data.user.id,
        text=data.text,
        stars=data.stars,
    )
    
    return JSONResponse(
        status_code=200,
        content=dict(detail='success')
    )


@router.get("/", response_model=List[Feedback])
async def get_feedbacks(
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> List[Feedback]:
    return await feedback_service.get_feedbacks(is_active=True)


@router.get("/{feedback_id}", response_model=Feedback)
async def get_one_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Feedback:
    return await feedback_service.get_one_feedback(id=feedback_id)


@router.get("/remove/{feedback_id}", response_model=JSONResponse)
async def remove_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    if not user_data.user.id in dev_config.admin.admins:
        raise MethodNotAllowedError

    await feedback_service.delete_feedback(feedback_id=feedback_id)

    return JSONResponse(
        status_code=200,
        content=dict(detail='success')
    )
    