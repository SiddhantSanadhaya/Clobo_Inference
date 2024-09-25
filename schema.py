from pydantic import BaseModel

class ImageUploadResponse(BaseModel):
    id: str

class ClassificationResultResponse(BaseModel):
    id: str
    result: str
    image_stored: bool
