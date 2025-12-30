from langchain_openai import ChatOpenAI  

DEFAULT_LLM={
    "model_name": "gpt-4.1",
    "temperature": 0.2
}

llm = ChatOpenAI(**DEFAULT_LLM)

