import requests
from src.openai.constants import PROMPT_PET_FEATURES
from src.openai.constants import PROMPT_COMPARE_PETS
from src.openai.config import OPENAI_API_KEY

def get_pet_features_client(url_image: str, max_tokens: int):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROMPT_PET_FEATURES
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url_image
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(f"Respuesta Pet features: {response.json()}")
    return response


def compare_pets_client(image_url_1: str, image_url_2: str, max_tokens: int):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROMPT_COMPARE_PETS
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url_1
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url_2
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(f"Respuesta Compare pets: {response.json()}")

    return response
