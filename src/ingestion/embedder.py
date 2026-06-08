import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def chunk_text(text: str):
    """텍스트를 청크로 분할"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    print(f"총 청크 수: {len(chunks)}개")
    return chunks

def save_to_faiss(chunks: list, save_path: str = "data/processed/faiss_index"):
    """청크를 임베딩해서 FAISS에 저장"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GOOGLE_API_KEY
    )
    
    vectorstore = FAISS.from_texts(chunks, embeddings)
    os.makedirs(save_path, exist_ok=True)
    vectorstore.save_local(save_path)
    print(f"FAISS 저장 완료: {save_path}")
    return vectorstore

if __name__ == "__main__":
    # pdf_parser.py에서 뽑은 텍스트 테스트
    sample_text = """
    삼성전자주식회사 임원 주요주주 특정증권등 소유상황보고서
    보고자: 이헌
    보고일: 2026년 6월 4일
    보유주식수: 1000주
    """
    
    chunks = chunk_text(sample_text)
    print("\n첫 번째 청크:")
    print(chunks[0] if chunks else "없음")
    
    vectorstore = save_to_faiss(chunks)
    print("\n벡터 저장 완료!")