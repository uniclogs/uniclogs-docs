# CoSI

Cosmos Satnogs/SpaceTrack Interface

***

# Prerequisite Services:

These services are expected to be running before `cosi-runner` can start.

* Mock OreSat
* COSMOS Command and Telemetry Server *(managed via Docker image)*
* COSMOS DART Service *(managed via Docker image)*
* PostgreSQL Daemon


## Mock Oresat

A mock of OreSat has been provided to stand in place of the actual satellite when integrating COSMOS tools into development.

**Start Mock-OreSat:**

`$` `python3 ./cosmos/mocks/oresat.py`

## COSMOS Install

A docker image has been provided to make the development experience more seamless while allowing COSMOS to operate in the environment it needs. This docker image is based off the official [BallAerospace COSMOS Image](https://hub.docker.com/r/ballaerospace/cosmos) but has been modified to include configurations and settings needed for UniClOGS.

**Install and run `ms-cosmos` from DockerHub:**

`$` `docker pull dmitrimcguuckin/ms-cosmos`

`$` `docker run --tty --interactive --detach --name cosmos --network=host --ipc=host --env DART_DB=$DART_DB --env DART_USERNAME=$COSI_USERNAME --env DART_PASSWORD=$COSI_PASSWORD --env DISPLAY=$DISPLAY --volume $XAUTH:/root/.Xauthority --volume /var/run/postgresql/.s.PGSQL.5432:/var/run/postgresql/.s.PGSQL.5432 dmitrimcguuckin/ms-cosmos`

`$` `docker attach cosmos`

**Note:** *The variables beginning with DART are expected to exist by COSMOS, and can be provided either manually or they can be exported as environment variables in a `.bashrc` file. Either way, they are required in order to forward the details to the container and to COSMOS.*

## PostgreSQL

Visit the [official PostgreSQL website](https://www.postgresql.org/download/) for instructions on how best to install on your system.


## CoSI Runner

#### Installation

`$` `pip install -r requirements.txt`

#### Development Dependencies Installation

`$` `pip install -r dev-requirements.txt`

#### Unit Tests

`$` `pytest tests/*`

#### Usage

```
usage: cosi-runner [-h] [--latest-tle (NORAD ID|SATELLITE NAME)] [-n NORAD_ID] [--no-satellite] [--no-telemetry]
[--no-tle] [-p POLL_INTERVAL] [-v]

Daemon for CoSI.

optional arguments:
  -h, --help            show this help message and exit
  --latest-tle (NORAD ID|SATELLITE NAME)
    [Default: 43793 (CSim)] Displays the latest TLE stored in DART DB either by Norad ID or by
satellite name
  -n NORAD_ID, --norad-id NORAD_ID
    [Default: 43793 (CSim)] Norad Satellite ID to use when fetching TLE and Telemetry
  --no-satellite        Disables fetching the latest satellite info from https://db.satnogs.org
  --no-telemetry        Disables fetching the latest telemetry from https://db.satnogs.org
  --no-tle              Disables fetching the latest Two Line Element (TLE) from https://space-track.org
  -p POLL_INTERVAL, --poll-interval POLL_INTERVAL
    [Default: 30m] Time interval at which CoSI polls spacetrack and satnogs for data
  -v, --verbose         Enable additional debug information
```

#### Example Commands

**Run CoSI with the Norad ID 965 every 10 minutes**

`$` `./cosi-runner --norad-id 965 -p 10m`


**Run CoSI every hour skipping fetching satellite info**

`$` `./cosi-runner -p 1h --no-satellite`

**Useful Links:**

* [`ballcosmos` Infinite Wait Fix](https://github.com/BallAerospace/python-ballcosmos/commit/377552e91ffafea76acedee8cb7ada1abc202898)
* [`ballcosmos` Commands Demonstration](https://github.com/BallAerospace/python-ballcosmos/blob/master/examples/test_json_drb.py)
