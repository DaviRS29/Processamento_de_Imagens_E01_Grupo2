from pydantic import BaseModel
from typing import Optional

class ProcessamentoImagemResponse(BaseModel):
    message: str
    filename: Optional[str] = None
    processed_image_url: Optional[str] = None
    file_base64: Optional[str] = None