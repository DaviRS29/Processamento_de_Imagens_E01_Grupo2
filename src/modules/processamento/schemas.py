from pydantic import BaseModel
from typing import Optional
import base64


class ProcessamentoImagemResponse(BaseModel):
    file_base64: Optional[str] = None
    message: str
    filename: Optional[str] = None
    processed_image_url: Optional[str] = None