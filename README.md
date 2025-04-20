 # Email Classification API with PII Masking

   This project provides an API for classifying support emails into different categories while masking personally identifiable information (PII).

   ## Features

   - Email classification into support categories (Billing, Technical Support, etc.)
   - Automatic PII detection and masking (names, emails, phone numbers, etc.)
   - API for processing and classifying emails

   ## API Usage

   ### Classify Email Endpoint

   **URL**: `/classify-email`  
   **Method**: POST  
   **Content-Type**: application/json  

   **Request Body**:
   ```json
   {
     "input_email_body": "Your email content here"
   }
   ```

   **Response**:
   ```json
   {
     "input_email_body": "Original email",
     "list_of_masked_entities": [
       {
         "position": ["start", "end"],
         "classification": "entity_type",
         "entity": "original_value"
       }
     ],
     "masked_email": "Masked email content",
     "category_of_the_email": "Category"
   }
   ```

   ## Setup Instructions

   1. Clone this repository
   2. Install dependencies: `pip install -r requirements.txt`
   3. Run the server: `uvicorn app:app --reload`
   4. Access the API at http://localhost:8000
   5. Documentation available at http://localhost:8000/docs

   ## Project Structure

   - `app.py`: Main application file
   - `api/`: API endpoints and routing
   - `models/`: Classification model implementation
   - `preprocessing/`: Email preprocessing utilities
   - `utils/`: Utility functions including PII masking
