import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from core.settings import settings
from modules.processamento.schemas import ProcessamentoImagemResponse
from modules.processamento.service import ProcessamentoImagemService
from modules.processamento.utils import (
    decode_image,
    detect_image_size_and_format,
    get_file_size,
)

router = APIRouter(tags=["Processamento de Imagem"], prefix="/processamento")


@router.post("/processar-imagem", response_model=ProcessamentoImagemResponse)
def processar_imagem(
    imagem: UploadFile = File(...),
    pre_processamento: bool = False,
    segmentacao: bool = False,
    pos_processamento: bool = False,
    extracao_atributos: bool = False,
    classificacao_reconhecimento: bool = False,
):
    service = ProcessamentoImagemService()
    file_obj = imagem.file
    tamanho_bytes = get_file_size(file_obj)
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if tamanho_bytes > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo muito grande. Máximo {settings.MAX_FILE_SIZE_MB}MB",
        )

    fmt, dims = detect_image_size_and_format(file_obj)
    if fmt not in settings.ALLOWED_FORMATS:
        formatos_str = ", ".join(settings.ALLOWED_FORMATS).upper()
        raise HTTPException(
            status_code=400, detail=f"Formato não suportado. Use {formatos_str}."
        )

    if not dims:
        raise HTTPException(
            status_code=400, detail="Não foi possível obter a resolução da imagem."
        )

    largura, altura = dims
    if largura < settings.MIN_WIDTH or altura < settings.MIN_HEIGHT:
        raise HTTPException(
            status_code=400,
            detail=f"Resolução mínima é {settings.MIN_WIDTH}x{settings.MIN_HEIGHT}. Fornecida: {largura}x{altura}.",
        )

    cv_image = decode_image(imagem)

    return service.processar_imagem(
        cv_image,
        pre_processamento,
        segmentacao,
        pos_processamento,
        extracao_atributos,
        classificacao_reconhecimento,
    )


@router.get("/download/{image_id}")
def download_processed_image(image_id: str):
    service = ProcessamentoImagemService()
    filepath = os.path.join(service.output_folder, f"{image_id}.jpg")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    return FileResponse(filepath, media_type="image/jpeg")
