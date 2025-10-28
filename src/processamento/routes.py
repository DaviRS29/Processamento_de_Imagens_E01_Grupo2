from fastapi import APIRouter
from fastapi import UploadFile, File

router = APIRouter(tags=["processamento-imagem"])


@router.post("/processar-imagem")
def processar_imagem(imagem: UploadFile = File(...)):
    return {"message": "Imagem processada com sucesso!"}
