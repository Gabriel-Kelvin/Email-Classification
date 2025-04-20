import subprocess
import sys

def download_spacy_model():
    print("Downloading spaCy model: en_core_web_sm")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    print("spaCy model downloaded successfully!")

if __name__ == "__main__":
    download_spacy_model()