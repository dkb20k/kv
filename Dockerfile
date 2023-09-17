FROM python:3-slim

RUN apt-get update; \
    apt-get install -y libmagic1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ADD main.py .
CMD ["python", "./main.py"]
