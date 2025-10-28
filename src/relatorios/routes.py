from fastapi import APIRouter

router = APIRouter(tags=["relatorios"])

@router.get("/relatorios")
def get_relatorios():
    return {"message": "Relatórios listados com sucesso!"}