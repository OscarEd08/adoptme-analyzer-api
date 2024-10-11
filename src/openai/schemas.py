from pydantic import BaseModel

class PetFeatures(BaseModel):
    prompt: str
    max_tokens: int = 300

class ComparePetsRequest(BaseModel):
    image_url_1: str
    image_url_2: str
    max_tokens: int = 300

class PetData(BaseModel):
    species: str
    breed: str
    age: int
    weight: int
    color: str
    size: str


class PetFeaturesResponse(BaseModel):
    status: int
    data: PetData | None