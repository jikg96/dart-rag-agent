import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_embeddings():
    """임베딩 모델 반환"""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

def split_text(text: str):
    """텍스트를 청크로 분할"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    print(f"청크 수: {len(chunks)}개")
    return chunks

def save_vectorstore(chunks: list, save_path: str = "data/processed/faiss_index"):
    """청크를 임베딩해서 FAISS에 저장"""
    embeddings = get_embeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    os.makedirs(save_path, exist_ok=True)
    vectorstore.save_local(save_path)
    print(f"벡터 저장 완료: {save_path}")
    return vectorstore

def load_vectorstore(save_path: str = "data/processed/faiss_index"):
    """저장된 FAISS 벡터 불러오기"""
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("벡터 불러오기 완료")
    return vectorstore

if __name__ == "__main__":
    sample_text = """
    삼성전자는 2024년 3분기 매출 79조원, 영업이익 9.1조원을 기록했습니다.
    전년 동기 대비 매출은 17% 증가했으며 영업이익은 274% 증가했습니다.
    반도체 부문에서 메모리 수요 회복으로 실적이 개선되었습니다.
    """

    chunks = split_text(sample_text)
    vectorstore = save_vectorstore(chunks)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    results = retriever.invoke("삼성전자 영업이익")
    print("\n검색 결과:")
    for doc in results:
        print(f"  - {doc.page_content}")