import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from utils.nlp import preprocess_text
from llm import generate_response

from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

email_router = APIRouter()

# class EmailInput(BaseModel):
#     text: str

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"txt", "pdf"}

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@email_router.post('/process_email')
async def process_email(
    text: str = Form(None), 
    file: UploadFile = File(None)
):
  email_process = preprocess_text(data.text)

  prompt = f"""
  Forneça uma classificação para o <<EMAIL>> utilizando a categorização PRODUTIVO ou IMPRODUTIVO, conforme a definição a seguir:
  - **Produtivo:** Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
  - **Improdutivo:** Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

  Responda somente com PRODUTIVO ou IMPRODUTIVO e adicione uma mensagem de sugestão automática que a pessoa que recebe o email possa dar.

  EMAIL: {email_process}
  """

  response = generate_response(prompt)

  return {response}
  # print(text_process)
  # return {"processed_text": text_process}
