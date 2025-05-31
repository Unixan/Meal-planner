FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system packages (git included)
RUN apt-get update && apt-get install -y git

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
