from fastapi import APIRouter, HTTPException
from src.openai.schemas import PetFeatures
from src.openai.client import get_pet_features_client
from src.openai.schemas import ComparePetsRequest
from src.openai.client import compare_pets_client

router = APIRouter()

@router.post("/get_pet_features/")
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
            "status": 404,
            "data": content.strip()
        }

    data = {}
    print(f"Contenido: {content}")
    for item in content.split(';'):
        key, value = item.split(':')
        key = key.strip()
        value = value.strip()

        if key == "Edad aproximada" or key == "Peso":
            value = int(value)

        if key == "Tamaño" and value.endswith('.'):
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

    return {
        "status": status_code,
        "data": content
    }