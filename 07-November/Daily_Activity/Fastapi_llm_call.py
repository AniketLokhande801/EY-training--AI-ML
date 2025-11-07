from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define request body schema
class Prompt(BaseModel):
    query: str

# POST endpoint for text generation
@app.post("/generate")
async def generate_response(prompt: Prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can change this to "gpt-4-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.query}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
