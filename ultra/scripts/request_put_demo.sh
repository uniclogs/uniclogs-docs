source ./common.sh
curl -X PUT -H "Content-Type: application/json" -H "token: $1" -d "$3" "$DOMAIN/request/$2"
