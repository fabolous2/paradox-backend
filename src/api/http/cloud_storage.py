import io

from fastapi import APIRouter, File, UploadFile

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.services import YandexStorageClient


router = APIRouter(
    prefix="/cloud-storage",
    tags=["Cloud Storage"],
    route_class=DishkaRoute,
)


@router.post("/upload-file")
async def upload_file(
    yandex_storage_client: FromDishka[YandexStorageClient],
    file: UploadFile = File(...),
) -> dict:
    content = await file.read()
    file_like_object = io.BytesIO(content)
    uploaded_file_url = await yandex_storage_client.upload_file(file_like_object, file.filename)

    return {"url": uploaded_file_url}
