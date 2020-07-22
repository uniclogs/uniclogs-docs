REQUEST_ID=$1
if [[ -z "$REQUEST_ID" ]]; then
    echo "missing request id in args"
    exit 0
fi

curl -X Put -H "Content-Type: application/json" -d '{"user_token": "fake user token", "latitude":45.512778, "longitude":-122.685278, "aos_utc": "2020-07-26T04:21:14.555000+00:00", "los_utc": "2020-07-26T04:31:44.337000+00:00"}' http://127.0.0.1:5000/request/REQUEST_ID
