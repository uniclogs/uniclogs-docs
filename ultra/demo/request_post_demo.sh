echo "Trying valid pass"
curl -X POST -H "Content-Type: application/json" -d '{"user_token": "fake user token", "latitude":45.512778, "longitude":-122.685278, "aos_utc": "2020-07-24T04:20:00.681000+00:00", "los_utc": "2020-07-24T04:30:33.790000+00:00"}' http://127.0.0.1:5000/request

echo ""

echo "Trying invalid pass"
curl -X POST -H "Content-Type: application/json" -d '{"user_token": "fake user token", "latitude":45.512778, "longitude":-122.685278, "aos_utc": "2020-07-24T04:20:00.681000+00:00", "los_utc": "2020-09-24T04:30:33.790000+00:00"}' http://127.0.0.1:5000/request
