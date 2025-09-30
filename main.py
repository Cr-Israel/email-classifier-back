from fastapi import FastAPI

app = FastAPI()

from routes.email import email_router

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(email_router)