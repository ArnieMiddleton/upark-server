# UPark-server

This project is the code that controls the backend server of the UPark application project. It acts as the intermediary between the database and the client application. It is responsible for handling all the requests from the client and returning the appropriate responses. It handles all communication with the project database.

## Information
It uses docker to build and deploy the service using `gunicorn` as the WSGI server. It is build using the `Flask` framework. It is deployed using the Google Cloud Platform's Cloud Run service.


## Setup
To run the server, you need to have credentials to access the database. These must be stored in a environment variables for the project. They should contain the following variables:
```
DB_USERNAME = <yourUsername>
DB_PASSWORD = <yourPassword>
DB_HOST = <dabaseHost>
DB_NAME = <databaseName>
```
These .env files should exist in the `dev`, `test`, and root directories of the project. The `dev` and `test` directories should contain the appropriate credentials for the respective environments. The root directory should contain the credentials for the production environment.

Additionally, `cert.pem` and `key.pem` files should be placed in the root directory of the project. These files are used to secure the connection between the client and the server. They should be generated using the following command:
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Local Deployment
To deploy the server locally, you need to have docker installed on your machine. You can install it by following the instructions [here](https://docs.docker.com/get-docker/).

Once you have docker installed, you can run the following commands to build and run the server:
```
docker compose build [prod|dev|test]
docker compose up [prod|dev|test]
```
This will build the server and run it on your local machine. You can access the prod server by going to `http://localhost:8080/`. The **prod** server is hosted on port `8080` with **dev** on `8081` and **test** on `8082`. You can stop the server by running the following command:
```
docker compose down
```

## GCloud Deployment
Ensure that you have the gcloud CLI installed on your machine. You can install it by following the instructions [here](https://cloud.google.com/sdk/docs/install).

To deploy the server to the Google Cloud Platform, you need to have the appropriate permissions to access the project. Additionally you need to enable the cloud run API, the cloud build API, and the Artifact Registry API. There are instructions for this [here](https://cloud.google.com/build/docs/build-push-docker-image). We will be deploying the server by creating a docker image and pushing it to the Google Cloud Artifact Registry. We will then deploy the image to the Cloud Run service.

There already exists a Docker image for the server in the root directory of the project. We will be pushing this image to the Artifact Registry. To do this we first need a repository in the Artifact Registry. If you do not have one, create one by running the following command:
```
gcloud artifacts repositories create [REPO_NAME] --repository-format=docker \
    --location=[LOCATION] --description="[REPOSITORY_DESCRIPTION]"
```
Replace the `[REPO_NAME]`, `[LOCATION]`, and `[REPOSITORY_DESCRIPTION]` with the appropriate values. You can verify that the repository was created by running the following command:
```
gcloud artifacts repositories list
```
Be aware that there are some restrictions on the ability to use cloud build for some locations for some projects. If you have issues with the location, you can change the location of the repository to a location that is supported by your project. More inforation can be found [here](https://cloud.google.com/build/docs/locations#restricted_regions_for_some_projects).

Once you have a repository, you can push the image to the repository by running the following commands:

First, get the Google Cloud project ID by running the following command:
```
gcloud config get-value project
```
Then, from the root directory of the project, run the command:
```
gcloud builds submit --tag "[LOCATION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/[IMAGE_NAME]:[TAG]"
```
You can also go to [this link](https://console.cloud.google.com/artifacts) to view the repository, and copy the location and name of the repo to the command above. Replace `[LOCATION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]` with the copied value.

Once the image is pushed to the repository, you can deploy the image to the Cloud Run service by running the following command:
```
gcloud run deploy [SERVICE_NAME] --image="[LOCATION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/[IMAGE_NAME]:[TAG]" --platform=managed --region=[REGION] --allow-unauthenticated
```
Replace `[SERVICE_NAME]`, `[LOCATION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]`, `[REGION]` with the appropriate values. You can also go to [this link](https://console.cloud.google.com/run) to view the service, and copy the region to the command above.

You can also deploy the server by going to the [Cloud Run](https://console.cloud.google.com/run) service on the Google Cloud Platform, and clicking on the `Deploy` button. You can then select the image from the Artifact Registry and deploy it to the Cloud Run service.