FROM python:3.11-slim

RUN pip install flask requests[socks]

COPY app.py /app/app.py
WORKDIR /app

CMD ["python", "app.py"]
