from fastapi import FastAPI
from pydantic import BaseModel
from parser import extract_fields

app = FastAPI()

class ParseRequest(BaseModel):
    text: str

@app.post("/parse")
def parse_text(req: ParseRequest):
    fields = extract_fields(req.text)
    return {"fields": fields}

@app.get("/health")
def health():
    return {"status": "ok"}