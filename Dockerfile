FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["sh","-c","guncorn -w 1 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT"]