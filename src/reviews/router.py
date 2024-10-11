import os
from fastapi import APIRouter, HTTPException, UploadFile, Query
from src.enums import FileType
from fastapi.responses import FileResponse
from src.reviews.client import get_reviews, create_reviews, get_sentiment
from src.reviews.schemas import TextInput
from src.database import db

router = APIRouter()

@router.get("/test-firebase-connection/")
def test_firebase_connection():
    try:
        # Intentar escribir un documento de prueba
        test_doc_ref = db.reference('test')
        test_doc_ref.set({'status': 'connected'})
        
        # Intentar leer el documento de prueba
        doc = test_doc_ref.get()
        if doc is None:
            raise HTTPException(status_code=500, detail="Error testing Firebase connection.")
        
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing Firebase connection: {str(e)}")

@router.post("/get_vet_reviews/")
def get_vet_reviews(file: UploadFile, file_type: FileType = Query(FileType.CSV)):
    try:        
        file_path = get_reviews(file.file, file_type)
                
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Error al generar el archivo.")
                
        return FileResponse(path=file_path, filename=file_path, media_type='application/octet-stream')
    
    except Exception as e:        
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
    
@router.post("/get_sentiment_review/")
def get_sentiment_review(request: TextInput):
    try:                
        sentiment = get_sentiment(request.text, request.lang)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
    
@router.post("/create_vet_collection/")
def get_vet_reviews_and_sentiment(file: UploadFile):
    try:
        response = create_reviews(file.file)

        if response:
            return {"status": 200, "message": "Colección creada exitosamente."}
        else:
            raise HTTPException(status_code=500, detail="Error al crear la colección de veterinarios.")        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")