source ./common.sh
curl -X POST -H 'Content-Type: application/json' -H  "token: $1" -d "$2" "$DOMAIN/request"
