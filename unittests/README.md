# Matchmaking Unit Tests 

The aim of unit tests is to test the matchmaking module isolated.
To this aim we have two sets of tests:

1) Core tests: they test the core functionalities of matchmaking using files as inputs (topology: i.e. agregator.json, and application descriptor: application.yaml)
2) API tests: This tests check the MATCH MAKING API using FastAPI locally.


## Local Installation Instructions

To get started, make sure you have Python installed. Then, open a terminal and run the following commands to install the required packages:

```bash
pip install fastapi
pip install uvicorn
pip install httpx
pip install pyyaml 
pip install requests
```



## Core tests

To run the unitests, just go into the unitests folder, add the unitest and the main path into PYTHONPATH environment variable and run the chosen tests as:
```
bash
export PYTHONPATH=.:..:$PYTHONPATH
python3 basic_test.py
```


## API tests


For the API tests we use [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
To test the Matchmaker code through the FastAPI, follow the steps:

### Start KeyCloak server:

In order to run The API we need to start a local KeyCloak server

```bash
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=change_me quay.io/keycloak/keycloak start-dev
```
This starts a KeyCloack server in http://localhost:8080, log in and through the visual API change the client: admin-cli to use Secure Authentication this will generate a Secret that we will need to to authenticate the FastAPI calls.

### Set up environment variables

The following environment variables should be set as follows, with the secret being updated to the one obtained from KeyCloak in the previous step.

```bash
export CLIENT_ID="admin-cli"
export CLIENT_SECRET="NIEzAv3WvzNaHTBOntZOKPz6kugvsF6M"
export URL_INTROESPECT="http://localhost:8080/realms/master/protocol/openid-connect/token/introspect"
export URL_TOKEN="http://localhost:8080/realms/master/protocol/openid-connect/token/"
export URL_AGGREGATOR="http://localhost:3000/agregator"
```

Alternatively modify the following file appropiately (with the correct secret) and run:
```bash
source ./testing_env.sh
```

To test that the token system is working, the scripts in tools folder: get_token.sh will output the token that can be tested with try_token.sh (the scripts use the curl comand).


### Alternatively: local agregator, remote token system

To test with the remote token system you can skip point 1 "Setup the keyClock Server" and configure the variables as follows:

```bash
export CLIENT_ID=icos-dev-matchmaker
export CLIENT_SECRET=5Ag0gNVrZGKXiUGZMdW2GUX3MOsnyPUk
export URL_INTROESPECT=https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token/introspect
export URL_TOKEN=https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token
export URL_AGGREGATOR=http://localhost:3000/agregator
```


###  Starting up the API Server and testing the API

From this point, please refer to the instructions in the main README.md file ../README.md, as the steps are the same.

# Legal
The Application Descriptor is released under the Apache license.
Copyright © 2022-2024 ICOS Consortium. All rights reserved.

🇪🇺 This work has received funding from the European Union's HORIZON research and innovation programme under grant agreement No. 101070177.
