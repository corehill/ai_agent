from langchain_openai import ChatOpenAI
from config.settings import DEEPSEEK_API_KEY, BASE_URL, LLM_TEMP

def create_llm(streaming: bool = True):
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=DEEPSEEK_API_KEY,
        base_url=BASE_URL,
        temperature=LLM_TEMP,
        streaming=streaming,
    )

llm = create_llm()