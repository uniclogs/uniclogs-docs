"""
Common JSON dictionary
======================

These dictionary are used by several input and output to ULTRA's endpoints.

Pass Data:
    - latitude : latitude decimal degrees as a float.
    - longitude : longitude decimal degrees as a float.
    - elevation_m : *optional* elevation in meter as a float.
    - horizon_deg : *optional* horizon degrees as a float.
    - aos_utc : aquisition of signal/satellite ISO 8601 datetime string
    - los_utc : loss of signal/satellite ISO 8601 datetime string

    Example ::

        {
            "latitude": 45.512778,
            "longitude": 122.68278,
            "elevation_m": 0.0
            "horizon_deg": 0.0
            "aos_utc": "2020-07-24T04:20:00.681000+00:00",
            "los_utc": "2020-07-24T04:30:33.790000+00:00"
        }

Public Endpoints
================

Passes Endpoint
===============
Restful API endpoint for calculating orbital passes for locations.
Endpoint is /passes.

GET
---

Input:
    JSON str
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - horizon_deg : horizon degrees as a float.

    Example: ::

        {
            "latitude": 45.512778,
            "longitude": 122.68278,
            "elevation_m": 0.0,
            "horizon_deg": 0.0
        }

Output:
    JSON str list of
        - latitude : latitude decimal degrees as a float.
        - longitude : longitude decimal degrees as a float.
        - elevation_m : *optional* elevation in meter as a float.
        - horizon_deg : *optional* horizon degrees as a float.
        - aos_utc : datetime string
        - los_utc : datetime string

    Example: ::

        [
            {
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "horizon_deg": 0.0
                "aos_utc": "2020-07-24T04:20:00.681000+00:00",
                "los_utc": "2020-07-24T04:30:33.790000+00:00"
            },
            {
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "horizon_deg": 0.0
                "aos_utc": "2020-07-24T05:57:19.612000+00:00",
                "los_utc": "2020-07-24T06:07:58.153000+00:00"
            },
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "horizon_deg": 0.0
                "aos_utc": "2020-07-24T07:34:11.719000+00:00",
                "los_utc": "2020-07-24T07:45:04.464000+00:00"
            }
        ]

Request List Endpoint
=====================
For add a new request to a user request list or getting the list of request
for a user. Endpoint is /replace.

POST
----

Restful API endpoint for add a new request for a user.

Input:
    JSON str
        - user_token : user's token.
        - pass_data : pass wanted by user

    Example: ::

        {
            "token": 12345
            "pass_data": {
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0,
                "aos_utc": "2020-07-24T07:34:11.753000+00:00",
                "los_utc": "2020-07-24T07:45:04.327000+00:00"
            }
        }

Output:
    A JSON message like
        {
            "message": "New request submitted. Request id: 12345"
        }

GET
---

Restful API endpoint for get a list of all request for a user.

Input:
    JSON str
        - user_token : user's token.

    Example: ::

        {
            "user_token": 12345
        }

Output:
    JSON str list of
        - request_id : the unique id for the request as a int,
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - aos_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        [
            {
                "request_id": 123,
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0
                "aos_utc": "2020-07-24T04:20:00.681000+00:00",
                "los_utc": "2020-07-24T04:30:33.790000+00:00"
            },
            {
                "request_id": 134,
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0,
                "aos_utc": "2020-07-24T05:57:19.612000+00:00",
                "los_utc": "2020-07-24T06:07:58.153000+00:00"
            },
                "request_id": 141,
                "latitude": 45.512778,
                "longitude": 122.68278,
                "elevation_m": 0.0,
                "aos_utc": "2020-07-24T07:34:11.719000+00:00",
                "los_utc": "2020-07-24T07:45:04.464000+00:00"
            }
        ]

Request Endpoint
================
For reading, replacing, or deleting a specific request.
Endpoint is /replace/<int>.

GET
---

Get a info for a user's request.

Input:
    JSON str
        - user_token : user's token.

    Example: ::

        {
            "user_token": 12345
        }

Output:
    JSON str list of
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - aos_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        {
            "latitude": 45.512778,
            "longitude": 122.68278,
            "elevation_m": 0.0
            "aos_utc": "2020-07-24T04:20:00.681000+00:00",
            "los_utc": "2020-07-24T04:30:33.790000+00:00"
        }

PUT
---

Replace the info for the user's request.

Input:
    JSON str
        - user_token : user's token.
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - aos_utc : datetime string

    Example: ::

        {
            "user_token": 12345
            "latitude": 45.512778,
            "longitude": 122.68278,
            "elevation_m": 0.0
            "aos_utc": "2020-07-24T04:20:00.681000+00:00",
            "los_utc": "2020-07-24T04:30:33.790000+00:00"
        }

Output:
    JSON str list of
        - latitude : latitude degrees as a float.
        - longitude : longitude degrees as a float.
        - elevation_m : elvation in meter as a float.
        - aos_utc : datetime string
        - stop_datetime_utc : datetime string

    Example: ::

        {
            "message": "modified request"
        }


DELETE
------

Delete the a user's request.

Input:
    JSON str
        - user_token : user's token.

    Example: ::

        {
            "user_token": 12345
        }

Output:
    JSON message
        - message : an error message or a success message

    Examples: ::

        {
            "message": "Request 12345 was deleted."
        }

        or

        {
            "message": "Permission denied."
        }

        or

        {
            "message": "Request 12345 was not found."
        }


"""
