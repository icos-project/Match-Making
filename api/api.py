# This file implements the FastAPI for Matchmaker service
from fastapi import FastAPI, HTTPException,Depends, Header, Body
from fastapi.responses import JSONResponse
import os
import httpx
from middlewares import JWTValidation, getUserToken, get_token
import requests
import re
from core.utils.dataformats import yaml_to_json_list,read_agregator_file
from core.main import matchmaking_main

app = FastAPI()

# Name of the input YAML file
yaml_file = 'Infra-taxonomy.yaml'
URL_AGGREGATOR  = os.environ.get('URL_AGGREGATOR')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


# EntryPoints

# Route to display a welcome message
@app.get('/')
def hello():
    return "Wellcome to MATCK MAKING API DEV"

@app.post('/getToken',response_model=dict)
def getTokenKeyCloak(json_data: dict):
    token = getUserToken(json_data)

    return token


#high_security = False
@app.post('/matchmake', response_model=dict, dependencies=[Depends(JWTValidation)])
async def matchmaking_service(yaml_content: str = Body(...), token: str = Depends(get_token)):
    
    print(yaml_content)
    try:
        # Uncomment the line below to read taxonomy from the local YAML file
        #taxonomy_json = yaml_to_json(yaml_file)
       
        taxonomy_json = {}

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Hacer la solicitud con el encabezado configurado
        async with httpx.AsyncClient() as client:
            response = await client.get(URL_AGGREGATOR, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            taxonomy_json = response.json()
        else:
            # Devolver una respuesta de error si la solicitud falla
            print('Error calling agregator at %s %s',URL_AGGREGATOR,headers)
            return JSONResponse(content={"error": "Error calling the agregator API"}, status_code=response.status_code)

        # Ahora puedes usar la variable 'taxonomy_json' que contiene la respuesta del endpoint del agregador
        #print(taxonomy_json)
        json_data = yaml_to_json_list(yaml_content)    
        #json_data = validate_yaml_body(yaml_content)

        if json_data:
            return matchmaking_main(json_data,taxonomy_json)
        else:     
            raise HTTPException(status_code=500, detail=f'Error converting YAML to JSON: {e}')
    except HTTPException as e:
        # Return an error response if an exception occurs during matchmaking
        return JSONResponse(content={"message": "Conversion failed", "detail": str(e)}, status_code=e.status_code)


# Route to return the content of 'agregator.json'
# This endpoint is only called when running locally 
@app.get('/agregator', response_model=dict,dependencies=[Depends(JWTValidation)])
#@app.get('/agregator', response_model=dict)
def agregator():
    
    print("Local agregator file being used")
    return read_agregator_file('agregator.json')


@app.post('/test', response_model=dict)
async def test_endpoint(json_data: dict):
    return {"message": "Received data", "data": json_data}


if __name__ == '__main__':
    import uvicorn
    print('Starting the FastAPI server at port 8000')
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
