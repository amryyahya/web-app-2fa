FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 python3-pip

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python3", "app.py"]