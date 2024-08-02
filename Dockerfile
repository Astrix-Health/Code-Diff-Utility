FROM python:3.8-slim

# Install dependencies
RUN apt-get update && apt-get install -y git
RUN pip install openai requests

# Set the working directory inside the container
WORKDIR /workspace

# Copy the script and entrypoint into the container
COPY generate_docs.py /workspace/generate_docs.py
COPY entrypoint.sh /workspace/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /workspace/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/workspace/entrypoint.sh"]
