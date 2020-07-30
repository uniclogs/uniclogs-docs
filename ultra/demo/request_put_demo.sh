REQUEST_ID=$1
if [[ -z "$REQUEST_ID" ]]; then
    echo "missing request id in args"
    exit 0
fi

curl -X PUT -H "Content-Type: application/json" -d '{"user_token": "test token", "latitude": 45.512778, "longitude": -122.685278, "aos_utc": "2020-07-30T06:02:32.784000+00:00", "los_utc": "2020-07-30T06:12:55.264000+00:00"}' http://127.0.0.1:5000/request/$REQUEST_ID

