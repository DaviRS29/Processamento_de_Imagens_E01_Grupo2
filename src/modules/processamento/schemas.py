from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ImageMetadata(BaseModel):
    image_id: str
    filename: Optional[str] = None
    filepath: Optional[str] = None
    file_base64: Optional[str] = None


class ProcessamentoImagemResponse(BaseModel):
    message: str
    generated_at: datetime
    image_metadata: ImageMetadata
