FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]