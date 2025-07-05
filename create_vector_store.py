import os
from openai import OpenAI
from dotenv import load_dotenv

def create_vector_store():
    """
    Creates an OpenAI vector store.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    client = OpenAI(api_key=api_key)

    # Create a vector store
    vector_store = client.beta.vector_stores.create(name="Big Beautiful Bill")

    # Save the vector store ID to a .env file
    with open(".env", "a") as f:
        f.write(f"\nVECTOR_STORE_ID={vector_store.id}\n")

    print(f"Vector Store created with ID: {vector_store.id}")
    print("Vector Store ID saved to .env file.")

if __name__ == "__main__":
    create_vector_store()
