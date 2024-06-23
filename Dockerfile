FROM ubuntu

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean

WORKDIR /app

COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

EXPOSE 5000

# Use the virtual environment to run the application
CMD ["venv/bin/python", "app.py"]
