FROM python:3.11.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory and copy app files
WORKDIR /upark-web-app-test
COPY ./app .
COPY ./test ./test
COPY ./gen ./gen
COPY ./test/.env .

# Install required packages
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8082

# Run the server
CMD gunicorn -b :8082 --timeout 0 -n upark-api -w 8 server:app