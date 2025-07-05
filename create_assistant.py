import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv

def create_assistant():
    """
    Creates an OpenAI Assistant with the 'Big Beautiful Bill' as its knowledge base.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    client = OpenAI(api_key=api_key)

    # Upload the knowledge base file
    try:
        with open("big_beautiful_bill.txt", "rb") as file:
            uploaded_file = client.files.create(file=file, purpose="assistants")
    except FileNotFoundError:
        print("Error: big_beautiful_bill.txt not found.")
        return

    # Create the assistant
    assistant = client.beta.assistants.create(
        name="Big Beautiful Bill Q&A",
        instructions="You are an expert on the 'Big Beautiful Bill'. Answer questions based on the provided text.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-turbo",
        file_ids=[uploaded_file.id],
    )

    # Save the assistant ID to a .env file
    with open(".env", "a") as f:
        f.write(f"\nASSISTANT_ID={assistant.id}\n")

    print(f"Assistant created with ID: {assistant.id}")
    print("Assistant ID saved to .env file.")

if __name__ == "__main__":
    create_assistant()
