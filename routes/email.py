from fastapi import APIRouter
from pydantic import BaseModel
from utils.nlp import preprocess_text

email_router = APIRouter()

class EmailInput(BaseModel):
    text: str


@email_router.post('/process_email')
async def process_email(data: EmailInput):
  text_process = preprocess_text(data.text)

  print(text_process)
  return {"processed_text": text_process}
