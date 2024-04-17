FROM python:3.11.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory and copy app files
WORKDIR /upark-web-app-dev
COPY ./app .
COPY ./gen ./gen
COPY ./dev/.env .

# Install required packages
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8081

# Generate data for the database from the production database
RUN python3 gen/copy-prod-dev.py
RUN python3 gen/gen-dummy-data.py

# Run the server
CMD gunicorn -b :8081 --timeout 0 -n upark-api -w 8 server:app