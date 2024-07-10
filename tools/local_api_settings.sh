docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=change_me quay.io/keycloak/keycloak start-dev
curl 'http://localhost:8080/realms/master/protocol/openid-connect/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=admin-cli' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'username=admin' \
--data-urlencode 'password=change_me'
cd ../api
uvicorn api:app --reload --host 0.0.0.0 --port 3000
uvicorn api:app --reload --host 0.0.0.0 --port 8000
