from fastapi import APIRouter, HTTPException
from src.openai.schemas import OpenAIRequest
from src.openai.client import get_pet_features_client

router = APIRouter()

@router.post("/get_pet_features/")
def get_pet_features(request: OpenAIRequest):
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
    for item in content.split(','):
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