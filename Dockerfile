FROM python:3.8-slim

# Install dependencies
RUN apt-get update && apt-get install -y git
RUN pip install openai requests

# Set the working directory inside the container
WORKDIR /workspace

# Copy the entire repository into the container
COPY . .

# Set the entrypoint to the script
ENTRYPOINT ["python", "/workspace/generate_docs.py"]
