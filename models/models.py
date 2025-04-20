# models.py
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailClassifier:
    def __init__(self, model_name="facebook/bart-large-mnli"):
        logger.info(f"Loading zero-shot classification model: {model_name}")
        self.classifier = pipeline("zero-shot-classification", model=model_name)

        # You can expand or modify this list based on the types of emails in your domain
        self.labels = [
            "Billing Issues",
            "Technical Support",
            "Account Management",
            "Subscription",
            "Login Problems",
            "Cancellation",
            "Refund"
        ]

    def predict_category(self, email_text: str) -> str:
        if not email_text.strip():
            return "Uncategorized"

        logger.info("Running zero-shot classification...")
        result = self.classifier(
            email_text,
            candidate_labels=self.labels,
            multi_label=False  # Only one category per email
        )

        logger.info(f"Prediction: {result['labels'][0]} with score {result['scores'][0]:.4f}")
        return result["labels"][0]
