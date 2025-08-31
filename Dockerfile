# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables to prevent Python buffering issues
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port your app will run on
EXPOSE 5000

# Run the app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
