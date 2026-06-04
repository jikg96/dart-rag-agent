"""'.env' 설정이 올바른지 빠르게 점검하는 스크립트.

사용법:
    python check_env.py
"""
import sys


def main() -> int:
    try:
        from src import config
    except RuntimeError as e:
        print(f"❌ 설정 오류: {e}")
        return 1

    print("✅ .env 로딩 성공")
    print(f"   DART_API_KEY        : {config.DART_API_KEY[:6]}...{config.DART_API_KEY[-4:]} (길이 {len(config.DART_API_KEY)})")
    print(f"   OPENAI_API_KEY      : {config.OPENAI_API_KEY[:7]}... (가려짐)")
    print(f"   LLM 모델            : {config.OPENAI_LLM_MODEL}")
    print(f"   임베딩 모델          : {config.OPENAI_EMBEDDING_MODEL}")
    print(f"   데이터 경로          : {config.DATA_DIR}")
    print(f"   벡터스토어 경로       : {config.VECTORSTORE_DIR}")

    if len(config.DART_API_KEY) != 40:
        print("⚠️  DART API 키는 보통 40자리입니다. 다시 확인해보세요.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
