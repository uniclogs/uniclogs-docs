source ./common.sh
curl -X GET -H "Content-Type: application/json" -H "token: $1" "$DOMAIN/request"
