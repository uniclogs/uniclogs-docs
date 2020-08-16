source ./common.sh
curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"$1\"}" "$DOMAIN/user"
