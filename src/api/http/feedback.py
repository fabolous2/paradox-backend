import uuid
from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.services import FeedbackService
from src.api.schema.feedback import CreateFeedback
from src.schema import Feedback


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    route_class=DishkaRoute,
)


@router.post("/post")
async def post_feedback(
    data: CreateFeedback,
    feedback_service: FromDishka[FeedbackService],
) -> JSONResponse:
    await feedback_service.add_feedback(
        id=uuid.uuid4(),
        product_id=data.product.id,
        user_id=data.user.id,
        text=data.text,
        stars=data.stars,
    )
    
    return JSONResponse(
        status_code=200,
        content=dict(message='success')
    )


@router.get("/", response_model=List[Feedback])
async def get_feedbacks(feedback_service: FromDishka[FeedbackService]) -> JSONResponse:
    feedbacks = await feedback_service.get_feedbacks(is_active=True)

    return JSONResponse(
        status_code=200,
        content=dict(message='success', feedbacks=feedbacks)
    )


@router.get("/{feedback_id}", response_model=Feedback)
async def get_one_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
) -> JSONResponse:
    feedback = await feedback_service.get_one_feedback(id=feedback_id)

    return JSONResponse(
        status_code=200,
        content=dict(message='success', feedback=feedback)
    )


@router.get("/remove/{feedback_id}", response_model=Feedback)
async def remove_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
) -> JSONResponse:
    await feedback_service.delete_feedback(feedback_id=feedback_id)

    return JSONResponse(
        status_code=200,
        content=dict(message='success')
    )
