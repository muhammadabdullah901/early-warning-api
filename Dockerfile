# Dockerfile — tells Hugging Face Spaces how to build and run the API.
# (Hugging Face builds this image and runs it for you, for free.)

FROM python:3.13-slim

# All our code lives in /app inside the container
WORKDIR /app

# Install dependencies first (so rebuilds are faster when only code changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Hugging Face Spaces sends web traffic to port 7860
EXPOSE 7860

# Start the FastAPI server on that port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
