from fastapi import APIRouter

router = APIRouter(tags=["Relatorios"])

@router.get("/relatorios")
def get_relatorios():
    return {"message": "Relatórios listados com sucesso!"}