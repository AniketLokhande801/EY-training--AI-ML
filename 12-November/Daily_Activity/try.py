from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import Docx2txtLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables
load_dotenv()

# Get API key and base URL from .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Initialize FastAPI app
app = FastAPI(title="AI Meeting Insights Generator")

# Initialize LLM (OpenRouter endpoint)
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",  # or another OpenRouter-supported model like "mistralai/mixtral"
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.3
)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["meeting_text"],
    template="""
You are an AI meeting analyst. Analyze the meeting transcript below and provide the following three structured outputs:

1. **Concise Meeting Summary**: Capture the overall discussion, decisions, and key points.
2. **Detailed Minutes of Meeting (MOM)**: Include topics discussed, decisions made, and next steps.
3. **List of Action Items**: Extract tasks with assigned persons and deadlines (if mentioned).

Meeting Transcript:
{meeting_text}

Format your response in clear sections with markdown headings:
### Meeting Summary
### Minutes of Meeting
### Action Items
"""
)

@app.post("/analyze_meeting")
async def analyze_meeting(file: UploadFile = File(...)):
    """Upload a Word file (.docx), extract text, and generate summary + MOM + tasks."""

    # Ensure file is .docx
    if not file.filename.endswith(".docx"):
        return JSONResponse(
            {"error": "Only .docx files are supported."}, status_code=400
        )

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            tmp_file.write(await file.read())
            tmp_path = tmp_file.name

        # Load content from docx
        loader = Docx2txtLoader(tmp_path)
        docs = loader.load()
        meeting_text = docs[0].page_content.strip()

        if not meeting_text:
            return JSONResponse(
                {"error": "No text content found in document."}, status_code=400
            )

        # Format the prompt
        prompt = prompt_template.format(meeting_text=meeting_text)

        # Invoke LLM
        response = llm.invoke(prompt)

        # Clean up temp file
        os.remove(tmp_path)

        return JSONResponse({"result": response.content})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)




