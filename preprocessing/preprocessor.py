import pandas as pd
import re


def load_dataset(path: str) -> pd.DataFrame:
    """
    Loads the dataset from a CSV file.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    df = pd.read_csv(path)

    # Optional sanity check: keep only rows with text in 'email' column
    df = df[df['email'].notnull()].reset_index(drop=True)

    return df


def clean_email_body(email: str) -> str:
    """
    Cleans the email body by removing extra whitespace and normalizing text.

    Args:
        email (str): Raw email string.

    Returns:
        str: Cleaned email string.
    """
    # Remove extra spaces, tabs, newlines
    email = re.sub(r'\s+', ' ', email)

    # Strip leading/trailing whitespace
    email = email.strip()

    return email


# Add this function for API integration
def preprocess_email(email: str) -> str:
    """
    Preprocesses a single email text.

    Args:
        email (str): Raw email text

    Returns:
        str: Preprocessed email text
    """
    return clean_email_body(email)


def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the dataset by cleaning email bodies and preserving originals.

    Args:
        df (pd.DataFrame): DataFrame containing the emails.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # Keep a copy of the original email for later demasking
    df['original_email'] = df['email']

    # Clean each email body
    df['email'] = df['email'].apply(clean_email_body)

    return df


if __name__ == "__main__":
    # For testing locally
    path = "../data/combined.csv"
    df = load_dataset(path)
    df = preprocess_dataset(df)
    print(df.head())