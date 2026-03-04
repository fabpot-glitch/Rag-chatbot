from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ USE A WORKING MODEL
MODEL_NAME = "mixtral-8x7b-32768"
# OR
# MODEL_NAME = "llama3-70b-8192"