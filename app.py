import gradio as gr
import sys
import os

# Add the current directory to the path to allow imports from project modules
sys.path.append(os.getcwd())

# Import your existing functions
from utils.pii_masker import mask_pii
from preprocessing.preprocessor import clean_email_body
from models.models import EmailClassifier

# Initialize the classifier
classifier = EmailClassifier()


def process_email(email_body):
    """
    Process an email through PII masking and classification

    Args:
        email_body (str): The raw email text

    Returns:
        dict: API response with masked entities and classification
    """
    # Step 1: Clean the email
    cleaned_email = clean_email_body(email_body)

    # Step 2: Mask PII
    # Your mask_pii function already returns a dict with the required structure
    result = mask_pii(cleaned_email)

    # Step 3: Classify the masked email
    masked_email = result["masked_email"]
    category = classifier.predict_category(masked_email)

    # Step 4: Update the result with the classification
    result["category_of_the_email"] = category

    return result


# Create Gradio interface
demo = gr.Interface(
    fn=process_email,
    inputs=gr.Textbox(lines=10, label="Email Body", placeholder="Enter the email text here..."),
    outputs=gr.JSON(),
    title="Email Classification System",
    description="This system classifies support emails into categories and masks personal information (PII).",
    examples=[
        [
            "Hello, my name is John Doe. I was born on 05/06/1992. You can reach me at john.doe@gmail.com or +91-9876543210. I'm having trouble with my monthly bill."],
        [
            "My name is Sarah Smith and I can't login to my account. My email is sarah@example.com and phone is 555-123-4567."]
    ]
)

# For local testing
if __name__ == "__main__":
    demo.launch()