import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # frontend local
    "http://localhost:5500",  # se acessar por localhost também
    # "http://meusite.com",   # depois você coloca seu domínio real aqui
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # quais origens podem acessar
    allow_credentials=True,
    allow_methods=["*"],           # métodos liberados (GET, POST, etc.)
    allow_headers=["*"],           # headers liberados
)

from routes.email import email_router

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(email_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)