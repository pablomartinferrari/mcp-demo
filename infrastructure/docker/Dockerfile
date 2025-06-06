FROM python:3.11-slim

WORKDIR /app

# Copy the server code and requirements
COPY main.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Use -u flag to ensure unbuffered output
ENTRYPOINT ["python", "-u", "main.py"]
