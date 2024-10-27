import io

from fastapi import APIRouter, File, UploadFile, Depends

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import YandexStorageClient


router = APIRouter(
    prefix="/cloud-storage",
    tags=["Cloud Storage"],
)


@router.post("/upload-file")
@inject
async def upload_file(
    yandex_storage_client: YandexStorageClient = Depends(Provide[Container.yandex_storage_client]),
    file: UploadFile = File(...),
) -> dict:
    content = await file.read()
    file_like_object = io.BytesIO(content)
    uploaded_file_url = await yandex_storage_client.upload_file(file_like_object, file.filename)

    return {"url": uploaded_file_url}
