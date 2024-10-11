import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.enums import FileType
from src.database import db
from src.reviews.config import comprehend

def get_reviews(data_set, file_type: FileType):    
    df = __transform_reviews(data_set)

    # Save the file and return the file path
    file_path = 'reviews_modified.csv' if file_type == FileType.CSV else 'reviews_modified.json'
    if file_type == FileType.CSV:
        df.to_csv(file_path, index=False)
    elif file_type == FileType.JSON:
        df.to_json(file_path, orient='records', lines=False)    
    
    return file_path

def get_sentiment(text: str, lang: str):      
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode=lang)
    return sentiment

def create_reviews(data_set):
    reviews = __get_reviews_with_sentiment(data_set)
    
    # Obtener los place_id existentes de la base de datos
    existing_place_ids = set()
    docs = db.reference('vets').get()
    if docs is not None:                
        existing_reviews = docs.get('vets', [])
        existing_place_ids = {review['place_id'] for review in existing_reviews}
    else:
        db.reference('vets').set({review['place_id']: review for review in reviews})
        return reviews
    
    # Filtrar los nuevos registros para eliminar duplicados
    unique_reviews = [review for review in reviews if review['place_id'] not in existing_place_ids]    
        
    if not unique_reviews:
        raise ValueError("No hay nuevos registros únicos para insertar.")
    
    # Insertar los registros únicos en la base de datos ya creada
    db.reference('vets').update({review['place_id']: review for review in unique_reviews})
        
    return unique_reviews

def __get_reviews_with_sentiment(data_set, num_vets=None):
    df = __transform_reviews(data_set)
    reviews = df.to_dict(orient='records')  

    if num_vets is not None:
        reviews = reviews[:num_vets]

    # Obtener los place_id existentes de la base de datos
    existing_reviews = db.reference('vets').get()
    existing_place_ids = {}
    if existing_reviews is not None:
        existing_place_ids = {review['place_id']: review for review in existing_reviews.get('vets', [])}

    def process_detailed_review(detailed_review, place_id):
        try:
            # Verificar si el place_id no existe o si la clave "reviews" es 0
            if place_id not in existing_place_ids or existing_place_ids[place_id].get('reviews', 1) == 0:
                sentiment = get_sentiment(detailed_review['review_translated_text'], 'es')
                detailed_review['sentiment'] = sentiment
            else:
                detailed_review['sentiment'] = None
        except Exception as e:
            detailed_review['sentiment'] = None
            print(f"Error processing sentiment for review {detailed_review['review_id']}: {e}")
        return detailed_review

    with ThreadPoolExecutor() as executor:
        futures = []
        for review in reviews:
            detailed_reviews = review['detailed_reviews']
            place_id = review['place_id']
            for detailed_review in detailed_reviews:
                futures.append(executor.submit(process_detailed_review, detailed_review, place_id))
        
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions caught during processing

    return reviews  

def __transform_reviews(data_set):
    df = pd.read_csv(data_set)    
    df['detailed_reviews'] = df['detailed_reviews'].apply(json.loads)

    # Filter out reviews with no translated text
    df['detailed_reviews'] = df['detailed_reviews'].apply(
        lambda reviews: [
            {
                'review_id': review.get('review_id'),
                'rating': review.get('rating'),
                'review_translated_text': review.get('review_translated_text'),
                'published_at_date': review.get('published_at_date'),
                'sentiment': None
            } for review in reviews if review.get('review_translated_text') is not None
        ]
    )

    # Filter out required columns and return the dataframe
    required_columns = ['place_id', 'name', 'rating', 'reviews', 'main_category', 'address', 'link', 'detailed_reviews']
    df = df[required_columns]

    return df