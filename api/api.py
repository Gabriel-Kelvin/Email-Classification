# api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.models import EmailClassifier

# Import the correct functions from your modules
# Note: You need to create a preprocess_email function in preprocessor.py
from preprocessing.preprocessor import clean_email_body as preprocess_email
from utils.pii_masker import mask_pii

router = APIRouter()
classifier = EmailClassifier()

class EmailRequest(BaseModel):
    input_email_body: str

@router.post("/classify-email")
def process_and_classify_email(request: EmailRequest):
    try:
        email_body = request.input_email_body

        # Step 1: Preprocess
        preprocessed = preprocess_email(email_body)

        # Step 2: Mask PII
        # Note: Your mask_pii function returns a dictionary, not two values
        pii_result = mask_pii(preprocessed)
        masked_email = pii_result["masked_email"]
        entities = pii_result["list_of_masked_entities"]

        # Step 3: Classify the masked email
        category = classifier.predict_category(masked_email)

        # Step 4: Construct strict API response
        response = {
            "input_email_body": email_body,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")