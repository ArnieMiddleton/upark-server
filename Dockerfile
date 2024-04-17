FROM python:3.11.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory and copy app files
WORKDIR /upark-web-app
COPY ./app .

# Install required packages
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

#CMD gunicorn --certfile cert.pem --keyfile key.pem -b :8080 --timeout 0 server:app
CMD gunicorn -b :8080 --timeout 0 server:app