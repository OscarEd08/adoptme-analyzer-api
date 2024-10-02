from fastapi import APIRouter, HTTPException
from src.aws.schemas import ComprehendRequest
from src.aws.client import comprehend_client

router = APIRouter()

@router.post("/comprehend/")
def get_comprehend_response(request: ComprehendRequest):
    try:
        response = comprehend_client.detect_sentiment(
            Text=request.text,
            LanguageCode=request.language_code
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response
