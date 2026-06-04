from dotenv import load_dotenv
import os

load_dotenv()

dart_key = os.getenv("DART_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

print("DART API KEY:", dart_key[:5] + "..." if dart_key else "없음")
print("GOOGLE API KEY:", google_key[:5] + "..." if google_key else "없음")