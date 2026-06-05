from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("SUCCESS")
    for model in list(models.data)[:10]:
        print(model.id)
except Exception as e:
    print("ERROR:", e)