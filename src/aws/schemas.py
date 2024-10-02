from pydantic import BaseModel

class ComprehendRequest(BaseModel):
    text: str
    language_code: str = "en"
