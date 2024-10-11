from fastapi import APIRouter, HTTPException
from src.openai.schemas import PetFeatures, PetFeaturesResponse
from src.openai.client import get_pet_features_client
from src.openai.schemas import ComparePetsRequest
from src.openai.client import compare_pets_client

router = APIRouter()

@router.post("/get_pet_features/", response_model=PetFeaturesResponse)
def get_pet_features(request: PetFeatures):
    print(f"Prompt: {request.prompt}")
    response = get_pet_features_client(request.prompt, request.max_tokens)

    status_code = response.status_code
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.json())

    response_json = response.json()
    content = response_json['choices'][0]['message']['content']

    if content.strip() == "No existe ninguna mascota.":
        return {
            "status": 400,
            "data": None
        }

    data = {}
    print(f"Contenido: {content}")
    for item in content.split(';'):
        key, value = item.split(':')
        key = key.strip()
        value = value.strip()

        if key == "age" or key == "weight":
            value = int(value)

        if key == "size" and value.endswith('.'):
            value = value[:-1]

        data[key] = value

    return {
        "status": status_code,
        "data": data
    }

@router.post("/compare_pets/")
def compare_pets(request: ComparePetsRequest):
    response = compare_pets_client(request.image_url_1, request.image_url_2, request.max_tokens)

    status_code = response.status_code
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.json())

    response_json = response.json()
    content = response_json['choices'][0]['message']['content'].strip()

    if content.startswith("Son la misma mascota"):
        status_code = 200
    elif content.startswith("No es la misma mascota"):
        status_code = 400
    else:
        status_code = 422

    return {
        "status": status_code,
        "message": content
    }