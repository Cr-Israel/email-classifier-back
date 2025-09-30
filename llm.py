import os
from dotenv import load_dotenv
from langchain_openai import OpenAI

# Carregar variáveis do arquivo .env
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

prompt_test = """
  Forneça uma classificação para o <<EMAIL>> utilizando a categorização PRODUTIVO ou IMPRODUTIVO, conforme a definição a seguir:
  - **Produtivo:** Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
  - **Improdutivo:** Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

  EMAIL: Agendar reunião.
  """

def generate_response(prompt: str) -> str:
  try:
      if not openai_api_key:
          raise ValueError("Missing OPENAI_API_KEY in environment")
      llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.7, api_key=openai_api_key)
      response = llm.invoke(prompt)
      return response
  except Exception as e:
      # Surface the error to the caller for better visibility
      raise

if __name__ == "__main__":
    print(generate_response(prompt_test))