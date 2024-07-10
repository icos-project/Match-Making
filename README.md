# MATCH MAKING

This is a simple guide on how to install, run and test the MATCH MAKING (MM) module throught FastAPI.

## Installation

First of all, to use call the module through its API you need to get the credentials. 

### Creating Docker Registry Secret

Run the following command to login to harbor repository

```bash
docker login harbor.res.eng.it/icos-private
```

Run the following command to create a secret for accessing the Docker registry:

```bash
kubectl create secret docker-registry harbor-cred --docker-server=harbor.res.eng.it --docker-username=YOUR_USER --docker-password=YOUR_PASSWORD
```

Once you have the credentials, the MM module can be deployed in different ways: 
- Using Kubernetes (with or without Helm Charts), (# Kubernetes Deployment)
- Docker (#Docker Deployment), or
- Bare Python scripts (# Alternative Installation with Bare Python). 



### Kubernetes Deployment


#### With Helm charts

Configure the matchmaker-chart/matchmaker/value.yaml file

```yaml
matchmaker:
  clientID: icos-dev-matchmaker
  clientSecret: 5Ag0gNVrZGKXiUGZMdW2GUX3MOsnyPUk
  urlIntrospect: https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token/introspect
  urlToken: https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token
  urlAggregator: http://localhost:8000/agregator
```

Run the installation with helm charts

```bash
helm install matchmaker ./matchmaker
```

#### Without Helm chart

##### Configuring Environment Variables

Before deploying the Matchmaker API on Kubernetes, you need to fill in the values for the environment variables in the `env-configmap.yaml` file. Open the file and update the following fields:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: matchmaker-configmap
data:
  CLIENT_ID: your_client_id
  CLIENT_SECRET: your_client_secret
  URL_INTROESPECT: https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token/introspect
  URL_TOKEN: https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token
  URL_AGGREGATOR: your_aggregator_url
```

Replace `your_client_id`, `your_client_secret`, and `your_aggregator_url` with your actual values.

##### Applying ConfigMap and Deployment

Now, apply the ConfigMap and the Kubernetes deployment:

```bash
kubectl apply -f env-configmap.yaml
kubectl apply -f matchmaker-service-deployment.yaml
```
This will configure the necessary environment variables, create the Docker registry secret, and deploy the Matchmaker API on Kubernetes.

### Docker Deployment

You can use Docker to run the application. Follow these commands:

```bash
docker build -t matchmaker:v1.0 .
docker run -p 8000:8000 -e CLIENT_ID='value_client_id' -e CLIENT_SECRET='value_client_secret' -e URL_INTROESPECT='value_url_introespect' -e URL_TOKEN='value_url_token' -e URL_AGGREGATOR='value_url_aggregator' matchmaker:v1.0

```

This will build a Docker image tagged as matchmaker:v1.0 and run a container with the application, exposing it on port 8000. Adjust the port mapping (-p host_port:container_port) according to your preferences.

### Alternative Installation with Bare Python

To get started, make sure you have Python installed. Then, open a terminal and run the following commands to install the required packages:

```bash
pip install fastapi
pip install uvicorn
pip install httpx
pip install pyyaml 
pip install requests
```

The software used is [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
#### Exporting environment variables

The following environment variables should be set as follows, with the secret being updated to the one obtained from KeyCloak in the previous step.
```bash
export CLIENT_ID=icos-dev-matchmaker
export CLIENT_SECRET=5Ag0gNVrZGKXiUGZMdW2GUX3MOsnyPUk
export URL_INTROESPECT=https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token/introspect
export URL_TOKEN=https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token
export URL_AGGREGATOR=http://localhost:3000/agregator
```

####  Starting up the API server

Once the python dependencies are installed and the environment variables have been set, to run the MM API you need to update the PYTHONPATH variable and the API server can be started from the api folder, using the following command:
```bash
cd api
export PYTHONPATH=.:..:$PYTHONPATH
uvicorn api:app --reload --host 0.0.0.0 --port 3000
```

## Testing the MM Module 

The MM module exposes the following endpoints:

### 1. Hello Endpoint

- **Endpoint:** `/`
- **Method:** GET
- **Description:** Displays a welcome message.

### 2. Match Making Endpoint

- **Endpoint:** `/getToken`
- **Method:** POST
- **Request Payload:** JSON data with authentication keycloak details.
- **Response:** JSON response with the authentication keycloak token.
- **Example JSON data:**
```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "grant_type": "password",
  "username": "your_username",
  "password": "your_password"
}
```
An example is provided in unittests/bodyPostmanGetToken.txt

### 3. Match Making Endpoint

- **Endpoint:** `/matchmaker`
- **Method:** POST
- **Request Payload:** JSON data with container information.
- **Authentication:** Requires a valid authentication token with the `Bearer` authentication type.
- **Response:** JSON response with the best matching cluster and node.
- **Example JSON data:**

The Body of the request whould contain a valid yaml file following the syntax of the Application Descriptor. 
See the file ''' application.yaml''' inside the unittests folder.

# Legal
The Application Descriptor is released under the Apache license.
Copyright © 2022-2024 ICOS Consortium. All rights reserved.

🇪🇺 This work has received funding from the European Union's HORIZON research and innovation programme under grant agreement No. 101070177.
