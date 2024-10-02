from fastapi import FastAPI
# from src.aws.router import router as aws_router
from src.openai.router import router as openai_router

app = FastAPI()

# app.include_router(aws_router, prefix="/aws", tags=["aws"])
app.include_router(openai_router, prefix="/openai", tags=["openai"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the OpenAI and Amazon Comprehend API Proxy"}
