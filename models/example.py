from models import EmailClassifier

# Initialize the classifier
classifier = EmailClassifier()

# Classify an email
email_text = "I'm having trouble logging into my account. I've tried resetting my password three times."
category = classifier.predict_category(email_text)
print(f"Email category: {category}")