REQUEST_ID=$1
if [[ -z "$REQUEST_ID" ]]; then
    echo "missing request id in args"
    exit 0
fi

curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/request/$REQUEST_ID
