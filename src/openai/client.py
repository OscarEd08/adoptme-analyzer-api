import os
import requests

# Obtener la clave API de OpenAI desde las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def openai_client(url_image: str, max_tokens: int):
    print(f"URL de la imagen: {url_image}")
    print(f"Max tokens: {max_tokens}")
    print(f"Clave API de OpenAI: {OPENAI_API_KEY}")

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
                        "text": "Por favor, mira la imagen de la mascota que se encuentra adjunta y proporciona las siguientes características separadas por comas en una sola linea: Especie, Raza, Edad aproximada(Dame un numero), Peso (en kilogramos, solo el numero), Color, Tamaño (pequeño, mediano, grande). Como por ejemplo: Especie: Perro, Raza: Mestizo, Edad aproximada: 5, Peso: 25, Color: Marrón claro y negro, Tamaño: Mediano. Si no existe ninguna mascota en la imagen devolver el siguiente mensaje: No existe ninguna mascota."
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

    # Imprimir la respuesta completa del servidor
    print(response.status_code)
    print(response.headers)
    print(response.text)

    return response
