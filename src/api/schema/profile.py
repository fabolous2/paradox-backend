from pydantic import BaseModel


class UpdateProfilePhoto(BaseModel):
    photo_url: str
