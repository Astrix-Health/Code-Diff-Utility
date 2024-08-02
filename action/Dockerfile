FROM python:3.8-slim

# Install dependencies
RUN pip install openai requests json

# Copy the script into the container
COPY generate_docs.py /generate_docs.py

# Set the entrypoint to the script
ENTRYPOINT ["python", "/generate_docs.py"]
