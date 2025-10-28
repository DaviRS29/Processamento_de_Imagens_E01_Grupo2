from fastapi import FastAPI
import uvicorn
from processamento.routes import router as processamento_imagem_router
from relatorios.routes import router as relatorios_router
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(processamento_imagem_router)
app.include_router(relatorios_router)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
