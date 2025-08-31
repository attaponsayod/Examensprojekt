# Use slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (optional for documentation)
EXPOSE 5000

# Run Gunicorn using $PORT from Heroku
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:$PORT"]
