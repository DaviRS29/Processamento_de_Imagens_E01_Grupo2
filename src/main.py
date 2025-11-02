import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from modules.processamento.routes import router as processamento_imagem_router
from modules.relatorios.routes import router as relatorios_router

app = FastAPI(prefix="/v1")

app.include_router(processamento_imagem_router)
app.include_router(relatorios_router)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
