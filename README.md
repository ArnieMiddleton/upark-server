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

To deploy the server to the Google Cloud Platform, you need to have the appropriate permissions to access the project. Additionally you need to enable the cloud run API and the cloud build API. You can do this by following the instructions [here](https://cloud.google.com/run/docs/quickstarts/build-and-deploy).

Once you have the appropriate permissions and APIs enabled, you can deploy the server by running the following command:
```
gcloud run deploy [prod|dev|test]
```
It will then prompt for a code location. Assuming you ran the command from the root of the project, just hit enter. Next, it will prompt for a service name. Use whatever service name you would like for your project. For ours please use 'upark-web-server'. Finally, it will prompt for a region. Use the region that is closest to you. For us, we used 'us-west3'.

After running the command, it will take a few minutes to deploy the server. Once it is done, it will provide you with a URL that you can use to access the server. You can also find this URL in the Google Cloud Console under the Cloud Run section.