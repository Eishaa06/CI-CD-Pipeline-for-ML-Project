FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Train the model to ensure it exists
RUN python model/train.py

EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app/app.py"]