curl 'http://localhost:8080/realms/master/protocol/openid-connect/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_secret=L5zMxUyawvyt61v9yuf2P4t18hnhO2U3' \
--data-urlencode 'client_id=admin-cli' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'username=admin' \
--data-urlencode 'password=change_me'

