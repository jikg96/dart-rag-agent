import requests
import os
import zipfile
import io
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
DART_API_KEY = os.getenv("DART_API_KEY")

def download_disclosure(rcept_no: str, save_path: str = "data/raw"):
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
    text = ""
    with pdfplumber.open(file_path) as pdf:
        print(f"총 페이지 수: {len(pdf.pages)}")
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    print(f"추출된 텍스트 길이: {len(text)}자")
    return text

if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    
    rcept_no = "20260604000077"
    save_path, files = download_disclosure(rcept_no)
    
    for f in files:
        if f.endswith(".pdf"):
            pdf_path = os.path.join(save_path, f)
            text = parse_pdf(pdf_path)
            print("\n텍스트 앞부분:")
            print(text[:300])
        elif f.endswith(".xml"):
            xml_path = os.path.join(save_path, f)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            text = ET.tostring(root, encoding="unicode")
            print("\nXML 앞부분:")
            print(text[:300])