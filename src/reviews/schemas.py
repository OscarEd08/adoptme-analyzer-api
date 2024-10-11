from pydantic import BaseModel

class TextInput(BaseModel):
    text: str
    lang: str = 'es'