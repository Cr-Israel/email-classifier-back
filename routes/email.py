from fastapi import APIRouter
from pydantic import BaseModel
from utils.nlp import preprocess_text
from llm import generate_response

email_router = APIRouter()

class EmailInput(BaseModel):
    text: str

# email = """
#   Olá! Espero que está mensagem lhe encontre bem.

#   Por meio deste e-mail, faço uma solicitação de suporte técnico em minha unidade escolar.

#   Fico no aguardo do seu retorno, obrigado.
  
#   Atenciosamente, Carlos Israel!
# """

@email_router.post('/process_email')
async def process_email(data: EmailInput):
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
