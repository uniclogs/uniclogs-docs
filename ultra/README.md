# ULTRA (UniClOGS Live Telemetry and Request API)

A service for providing a public access interface to internal UniClOGS data.

## API Usage and Documentation

Extensive API usage and documentation can be found on our [Apiary Page](https://ultra.docs.apiary.io).

## Start the API Server
`$` `gunicorn --worker-tmp-dir /dev/shm --config ultra/__init__.py ultra:api`
