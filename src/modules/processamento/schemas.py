from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ImageMetadata(BaseModel):
    image_id: str = Field(..., description="Identificador único da imagem processada")
    filename: Optional[str] = Field(None, description="Nome do arquivo da imagem original")
    filepath: Optional[str] = Field(None, description="Caminho completo do arquivo processado no servidor")
    file_base64: Optional[str] = Field(None, description="Imagem processada codificada em base64")

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "550e8400-e29b-41d4-a716-446655440000",
                "filename": "image.jpg",
                "filepath": "processed_images/550e8400-e29b-41d4-a716-446655440000.jpg",
                "file_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
            }
        }


class ProcessamentoImagemResponse(BaseModel):
    message: str = Field(..., description="Mensagem descritiva do resultado do processamento")
    generated_at: datetime = Field(..., description="Data e hora em que a imagem foi processada")
    image_metadata: ImageMetadata = Field(..., description="Metadados da imagem processada")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Imagem processada com sucesso!",
                "generated_at": "2024-01-15T10:30:00",
                "image_metadata": {
                    "image_id": "550e8400-e29b-41d4-a716-446655440000",
                    "filename": "image.jpg",
                    "filepath": "processed_images/550e8400-e29b-41d4-a716-446655440000.jpg",
                    "file_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
                }
            }
        }
