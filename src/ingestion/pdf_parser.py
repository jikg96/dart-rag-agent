import requests
import os
import zipfile
import io
import pdfplumber
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

DART_API_KEY = os.getenv("DART_API_KEY")

def download_disclosure(rcept_no: str, save_path: str = "data/raw"):
    """공시 번호로 문서 다운로드"""
    url = "https://opendart.fss.or.kr/api/document.xml"
    params = {
        "crtfc_key": DART_API_KEY,
        "rcept_no": rcept_no
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    os.makedirs(save_path, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        z.extractall(save_path)
        extracted = z.namelist()
        print(f"압축 해제된 파일: {extracted}")

    return save_path, extracted

def parse_pdf(file_path: str) -> str:
    """PDF에서 텍스트 추출"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        print(f"총 페이지 수: {len(pdf.pages)}")
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    print(f"추출된 텍스트 길이: {len(text)}자")
    return text

def parse_xml(file_path: str) -> str:
    """XML에서 텍스트 추출"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    texts = []
    for elem in root.iter():
        if elem.text and elem.text.strip():
            texts.append(elem.text.strip())
    text = "\n".join(texts)
    print(f"추출된 텍스트 길이: {len(text)}자")
    return text

def extract_text(save_path: str, files: list) -> str:
    """PDF 또는 XML에서 텍스트 추출 후 반환"""
    full_text = ""

    for f in files:
        if f.endswith(".pdf"):
            print(f"PDF 파싱 중: {f}")
            full_text += parse_pdf(os.path.join(save_path, f))
        elif f.endswith(".xml"):
            print(f"XML 파싱 중: {f}")
            full_text += parse_xml(os.path.join(save_path, f))

    # 텍스트 파일로 저장
    processed_path = "data/processed"
    os.makedirs(processed_path, exist_ok=True)
    txt_file = os.path.join(processed_path, "disclosure.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"\n텍스트 저장 완료: {txt_file}")

    return full_text

if __name__ == "__main__":
    rcept_no = "20260604000077"
    save_path, files = download_disclosure(rcept_no)
    text = extract_text(save_path, files)
    print("\n텍스트 앞부분:")
    print(text[:300])
