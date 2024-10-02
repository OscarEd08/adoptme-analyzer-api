from fastapi import APIRouter, HTTPException
from src.openai.schemas import OpenAIRequest
from src.openai.client import openai_client

router = APIRouter()

@router.post("/completion/")
def get_openai_response(request: OpenAIRequest):
    print(f"Prompt: {request.prompt}")
    response = openai_client(request.prompt, request.max_tokens)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
