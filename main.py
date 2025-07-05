import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if not OPENAI_API_KEY or not ASSISTANT_ID:
    raise ValueError("Missing OPENAI_API_KEY or ASSISTANT_ID in .env file")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

class AskRequest(BaseModel):
    question: str
    thread_id: str | None = None

class AskResponse(BaseModel):
    answer: str
    thread_id: str
    status: str # "completed" or "requires_action"

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Receives a question and an optional thread_id, sends it to the OpenAI Assistant,
    and returns the answer or a clarifying question.
    """
    try:
        thread_id = request.thread_id
        if thread_id is None:
            thread = client.beta.threads.create()
            thread_id = thread.id
        
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=request.question
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            model="gpt-4o"
        )

        while run.status in ["queued", "in_progress"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

        if run.status == "requires_action":
            # For now, we'll just return the first tool call's arguments as a question
            # A more robust solution would handle multiple tool calls
            tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
            question = tool_call.function.arguments
            return AskResponse(answer=question, thread_id=thread_id, status="requires_action")

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_message = next((m for m in messages.data if m.role == "assistant"), None)

        if assistant_message:
            answer = assistant_message.content[0].text.value
            return AskResponse(answer=answer, thread_id=thread_id, status="completed")
        else:
            return AskResponse(answer="The assistant did not provide a response.", thread_id=thread_id, status="completed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
