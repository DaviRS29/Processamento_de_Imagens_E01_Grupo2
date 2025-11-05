import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from src.core.settings import settings
from src.modules.processamento.schemas import ProcessamentoImagemResponse
from src.modules.processamento.service import ProcessamentoImagemService
from src.modules.processamento.utils import (
    decode_image,
    detect_image_size_and_format,
    get_file_size,
)

router = APIRouter(tags=["Processamento de Imagem"], prefix="/processamento")


@router.post(
    "/processar-imagem",
    response_model=ProcessamentoImagemResponse,
    summary="Processa uma imagem",
    description="Recebe uma imagem e aplica transformações conforme os parâmetros fornecidos. "
    "Suporta formatos JPEG e PNG com resolução mínima de 256x256 pixels.",
    responses={
        200: {"description": "Imagem processada com sucesso"},
        400: {
            "description": "Erro de validação (arquivo inválido, formato não suportado, etc.)"
        },
        500: {"description": "Erro interno do servidor"},
    },
)
def processar_imagem(
    imagem: UploadFile = File(
        ..., description="Arquivo de imagem para processar (JPEG ou PNG)"
    ),
    pre_processamento: bool = File(
        False, description="Aplica técnicas de pré-processamento à imagem"
    ),
    pre_processamento_gamma: float = File(
        1.0, description="Fator de correção de brilho (gamma correction) [0.0 - 2.0]",
    ),
    segmentacao: bool = File(
        False,
        description="Converte a imagem para escala de cinza e aplica filtro Gaussian Blur",
    ),
    pos_processamento: bool = File(
        False, description="Aplica técnicas de pós-processamento à imagem"
    ),
    extracao_atributos: bool = File(
        False, description="Extrai atributos relevantes da imagem"
    ),
    classificacao_reconhecimento: bool = File(
        False, description="Realiza classificação e reconhecimento de padrões"
    ),
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

    if pre_processamento_gamma < 0.0 or pre_processamento_gamma > 2.0:
        raise HTTPException(
            status_code=400,
            detail="Fator de correção de brilho (gamma correction) deve estar entre 0.0 e 2.0.",
        )

    cv_image = decode_image(imagem)

    return service.processar_imagem(
        cv_image,
        pre_processamento,
        segmentacao,
        pos_processamento,
        extracao_atributos,
        classificacao_reconhecimento,
        pre_processamento_gamma,
    )


@router.get(
    "/download/{image_id}",
    summary="Baixa imagem processada",
    description="Retorna o arquivo de imagem processada a partir do ID fornecido",
    responses={
        200: {"description": "Arquivo de imagem processada"},
        404: {"description": "Imagem não encontrada com o ID fornecido"},
    },
)
def download_processed_image(image_id: str):
    service = ProcessamentoImagemService()
    filepath = os.path.join(service.output_folder, f"{image_id}.jpg")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    return FileResponse(filepath, media_type="image/jpeg")
