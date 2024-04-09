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
```

## GCloud Deployment
Ensure that you have the gcloud CLI installed on your machine. You can install it by following the instructions [here](https://cloud.google.com/sdk/docs/install).

To deploy the server to the Google Cloud Platform, you need to have the appropriate permissions to access the project. Additionally you need to enable the cloud run API and the cloud build API. You can do this by following the instructions [here](https://cloud.google.com/run/docs/quickstarts/build-and-deploy).

Once you have the appropriate permissions and APIs enabled, you can deploy the server by running the following command:
```
gcloud run deploy
```
It will then prompt for a code location. Assuming you ran the command from the root of the project, just hit enter. Next, it will prompt for a service name. Use whatever service name you would like for your project. For ours please use 'upark-web-server'. Finally, it will prompt for a region. Use the region that is closest to you. For us, we used 'us-west3'.

After running the command, it will take a few minutes to deploy the server. Once it is done, it will provide you with a URL that you can use to access the server. You can also find this URL in the Google Cloud Console under the Cloud Run section.