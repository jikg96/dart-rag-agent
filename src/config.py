"""환경 변수 로딩 및 설정 관리."""
import os
from pathlib import Path

from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 로드
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _require(name: str) -> str:
    """필수 환경 변수를 읽고, 없으면 친절한 에러를 발생시킨다."""
    value = os.getenv(name)
    if not value or value.startswith("your_"):
        raise RuntimeError(
            f"환경 변수 '{name}' 가 설정되지 않았습니다. "
            f".env 파일을 확인하세요 (.env.example 참고)."
        )
    return value


# ── API 키 ────────────────────────────────────────────────────
DART_API_KEY = _require("DART_API_KEY")
OPENAI_API_KEY = _require("OPENAI_API_KEY")

# ── 모델 ──────────────────────────────────────────────────────
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# ── 경로 ──────────────────────────────────────────────────────
DATA_DIR = PROJECT_ROOT / os.getenv("DATA_DIR", "./data").lstrip("./")
VECTORSTORE_DIR = PROJECT_ROOT / os.getenv("VECTORSTORE_DIR", "./vectorstore").lstrip("./")

DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
