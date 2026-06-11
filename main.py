import io
import json
import os
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "").strip('"\''))


app = FastAPI(title="Juris Node Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Underlying Business Logic Functions
async def run_gemini_analysis(text_content: str) -> dict:
    # Use gemini-2.5-flash-lite for higher free-tier request limits
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    prompt = f"Parse this contract: {text_content}"
    
    pure_native_schema = {
        "type": "OBJECT",
        "properties": {
            "overall_safety_score": {"type": "INTEGER"},
            "executive_summary": {"type": "STRING"},
            "recommendations": {"type": "ARRAY", "items": {"type": "STRING"}},
            "clauses": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "clause_title": {"type": "STRING"},
                        "extracted_text": {"type": "STRING"},
                        "risk_level": {"type": "STRING"},
                        "explanation": {"type": "STRING"}
                    },
                    "required": ["clause_title", "extracted_text", "risk_level", "explanation"]
                }
            }
        },
        "required": ["overall_safety_score", "executive_summary", "recommendations", "clauses"]
    }

    
    retries = 3
    delay = 10 
    
    for attempt in range(retries):
        try:
            gemini_call = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=pure_native_schema
                )
            )
            return json.loads(gemini_call.text)
        except exceptions.ResourceExhausted:
            if attempt == retries - 1:
                raise HTTPException(status_code=429, detail="Quota exceeded. Please retry later.")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history_index():
    """
    Temporary mock history endpoint to keep the frontend sidebar stable.
    """
    return [
        {
            "id": 1,
            "contract_name": "Sample_Employment_Bond.pdf",
            "overall_safety_score": 82,
            "executive_summary": "Standard non-compete clause with reasonable geofencing boundaries.",
            "recommendations": ["Review indemnity caps closely."],
            "clauses": []
        }
    ]

@app.post("/analyze")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """
    Intercepts the multipart form file upload from app.js, extracts the text,
    and streams structured data back to the dashboard layout.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Validation error: Target asset file format must be a PDF.")
        
    try:
        
        pdf_bytes = await file.read()
        
      
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        extracted_text = ""
        
        for page in doc:
            extracted_text += page.get_text()
            
        doc.close()
        
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400, 
                detail="The uploaded PDF contains no digital text layers. Please use a text-selectable document."
            )
            
        
        analysis_result = await run_gemini_analysis(extracted_text)
        
        
        analysis_result["contract_name"] = file.filename
        return analysis_result

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Processing Error: {str(e)}")

@app.post("/test-analysis")
async def test_analysis(payload: dict):
    return await run_gemini_analysis(payload.get("text", ""))