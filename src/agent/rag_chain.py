import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_retriever(index_path: str = "data/processed/faiss_index"):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vectorstore = FAISS.load_local(
        index_path, embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def build_chain():
    retriever = load_retriever()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )
    prompt = ChatPromptTemplate.from_template("""
당신은 금융 공시 분석 전문가입니다.
아래 공시 내용을 참고해서 질문에 답변하세요.
모르는 내용은 모른다고 하세요.

[공시 내용]
{context}

[질문]
{question}
""")
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

if __name__ == "__main__":
    chain = build_chain()
    answer = chain.invoke("삼성전자 영업이익은 얼마야?")
    print("\n답변:", answer)