# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV ASSISTANT_ID=$ASSISTANT_ID
ENV VECTOR_STORE_ID=$VECTOR_STORE_ID

# Run uvicorn when the container launches, using the PORT environment variable
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
