FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 pipx && \
    pipx ensurepath && \
    sudo pipx ensurepath --global

WORKDIR /app

COPY . /app

RUN pipx install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]