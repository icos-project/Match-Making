from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
from urllib.parse import urlencode
import urllib.parse
import json
import os

#CLIENT_ID="icos-dev-matchmaker"
#CLIENT_SECRET="5Ag0gNVrZGKXiUGZMdW2GUX3MOsnyPUk"
#URL_INTROESPECT="https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token/introspect"
#URL_TOKEN="https://keycloak.dev.icos.91.109.56.214.sslip.io/realms/icos-dev/protocol/openid-connect/token"

CLIENT_ID  = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
URL_INTROESPECT = os.environ.get('URL_INTROESPECT')
URL_TOKEN = os.environ.get('URL_TOKEN')

def getUserToken(data: json):

    # Codifica los valores de los parámetros
    encoded_username = urllib.parse.quote(data['username'])
    encoded_password = urllib.parse.quote(data['password'])

    payload = 'client_id='+data['client_id']+'&client_secret='+data['client_secret']+'&grant_type='+data['grant_type']+'&username='+encoded_username+'&password='+encoded_password
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    print(URL_TOKEN)
    print(headers)
    print(payload) 

    response = requests.request("POST", URL_TOKEN, headers=headers, data=payload)

    token = json.loads(response.text)
    
    return token

def get_token(authorization: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return authorization

def JWTValidation(token: str = Depends(get_token)):
    try:
        payload = 'client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET+'&token='+token
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        print(payload)
        print(headers)
        print(URL_INTROESPECT)
        response = requests.request("POST", URL_INTROESPECT , headers=headers, data=payload)

        print(response.text)
        valid = json.loads(response.text)['active']
        print(valid)

        if (not valid):
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return valid
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

