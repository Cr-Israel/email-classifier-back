import os
from dotenv import load_dotenv
# from langchain_openai import OpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage

# Carregar variáveis do arquivo .env
load_dotenv()

huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")



def generate_response(prompt: str) -> str:
  try:
      if not huggingfacehub_api_token:
          raise ValueError("Missing HUGGINGFACEHUB_API_TOKEN in environment")

      endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            task="conversational",
            huggingfacehub_api_token=huggingfacehub_api_token,
            temperature=0.7,
            # max_new_tokens=256,
        )

      llm = ChatHuggingFace(llm=endpoint)

      response = llm.invoke([HumanMessage(content=prompt)])
      return getattr(response, "content", str(response))
      
  except Exception as e:
      # Surface the error to the caller for better visibility
      raise

# if __name__ == "__main__":
#     print(generate_response(prompt_test))