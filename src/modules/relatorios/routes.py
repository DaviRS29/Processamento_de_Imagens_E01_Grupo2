from fastapi import APIRouter

router = APIRouter(tags=["Relatórios"], prefix="/relatorios")

@router.get(
    "",
    summary="Lista relatórios disponíveis",
    description="Retorna uma lista de todos os relatórios de processamento de imagens disponíveis no sistema",
    responses={
        200: {"description": "Lista de relatórios retornada com sucesso"}
    }
)
def get_relatorios():
    return {"message": "Relatórios listados com sucesso!"}