FROM python:3.13.3-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

RUN pip install --no-cache-dir --timeout=120 -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]