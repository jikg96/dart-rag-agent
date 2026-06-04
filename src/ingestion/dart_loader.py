import requests
import os
import zipfile
import io
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

DART_API_KEY = os.getenv("DART_API_KEY")

def get_corp_code(company_name: str):
    """회사명으로 DART 기업 코드 검색"""
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    params = {"crtfc_key": DART_API_KEY}
    
    res = requests.get(url, params=params)
    
    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        with z.open("CORPCODE.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()
    
    exact_match = None
    contains_match = None
    
    for corp in root.findall("list"):
        name = corp.findtext("corp_name")
        if name == company_name:
            exact_match = corp
            break
        elif company_name in name and contains_match is None:
            contains_match = corp
    
    result = exact_match if exact_match is not None else contains_match
    
    if result is not None:
        corp_code = result.findtext("corp_code")
        corp_name = result.findtext("corp_name")
        print(f"기업 찾음: {corp_name} → {corp_code}")
        return corp_code
    
    print("기업을 찾을 수 없습니다.")
    return None

def get_disclosure_list(corp_code: str):
    """기업 코드로 최근 공시 목록 조회"""
    url = "https://opendart.fss.or.kr/api/list.json"
    params = {
        "crtfc_key": DART_API_KEY,
        "corp_code": corp_code,
        "page_count": 10
    }
    res = requests.get(url, params=params)
    data = res.json()
    
    if data["status"] == "000":
        disclosures = data["list"]
        print(f"\n최근 공시 {len(disclosures)}건:")
        for d in disclosures:
            print(f"  - {d['rcept_dt']} | {d['report_nm']} | 공시자: {d['flr_nm']}")
        return disclosures
    else:
        print(f"공시 없음: {data['message']}")
        return []

if __name__ == "__main__":
    corp_code = get_corp_code("삼성전자")
    if corp_code:
        get_disclosure_list(corp_code)