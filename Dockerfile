FROM debian:11-slim

RUN apt-get update && \
    apt-get install -y python3-pip openjdk-11-jre-headless

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]