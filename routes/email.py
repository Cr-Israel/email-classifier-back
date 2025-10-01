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
  if not text and not file:
      raise HTTPException(status_code=400, detail="Envie um texto ou um arquivo (.txt ou .pdf)")

  email_content = ""

  # caso venha texto puro
  if text:
    email_content = text
    
  elif file:
    if not allowed_file(file.filename):
      raise HTTPException(status_code=400, detail="Formato de arquivo não permitido.")

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
      f.write(await file.read())

    # ler arquivo dependendo da extensão
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'txt':
      with open(filepath, 'r', encoding='utf-8') as f:
        email_content = f.read()
    elif ext == 'pdf':
      reader = PdfReader(filepath)
      email_content = "".join([page.extract_text() or "" for page in reader.pages])

  # pré-processamento
  email_process = preprocess_text(email_content)

  prompt = f"""
  Forneça uma classificação para o <<EMAIL>> utilizando a categorização PRODUTIVO ou IMPRODUTIVO, conforme a definição a seguir:
  - **Produtivo:** Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, agendamento de reuniões, fechamento de contratos, assuntos importantes, assuntos empresarias...).
  - **Improdutivo:** Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos, mensagens de propaganda, promoções...).

  Responda somente com PRODUTIVO ou IMPRODUTIVO e adicione uma mensagem de sugestão automática que a pessoa que recebe o email possa dar.
  Na sugestão automática, forneça apenas a mensagem, sem nenhum outro texto antes ou depois, a sugestão precisa ser relevante para a categoria que foi definada e o com o conteúdo do email.
  Se for classificado como IMPRODUTIVO: forneça uma mensagem extremamente curta e educada, demonstrando apenas que o email foi recebido, sem encorajar continuação da conversa. Exemplos: "Obrigado.", "Recebido.", "Agradecemos o contato."

  EMAIL: {email_process}
  """

  response = generate_response(prompt)
  
  # Parse the response to separate category and suggestion
  lines = response.strip().split('\n')
  category = ""
  suggestion = ""
  
  # Look for PRODUTIVO or IMPRODUTIVO in the response
  for line in lines:
    line = line.strip()
    if line.upper() in ['PRODUTIVO', 'IMPRODUTIVO']:
      category = line.upper()
      break
  
  # Extract suggestion (everything after the category)
  if category:
    category_index = response.upper().find(category)
    if category_index != -1:
      suggestion_start = category_index + len(category)
      suggestion = response[suggestion_start:].strip()
      # Remove common prefixes
      suggestion = suggestion.replace(':', '').strip()
  
  return {
    "category": category,
    "suggestion": suggestion
  }
  # print(text_process)
  # return {"processed_text": text_process}
