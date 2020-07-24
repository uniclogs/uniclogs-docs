# CoSI

Cosmos Satnogs/SpaceTrack Interface

***

# Prerequisite Services:

These services are expected to be running before `cosid.py` can run.

* Mock OreSat
* COSMOS Command and Telemetry Server
* PostgreSQL Daemon


## Mock Oresat

A mock of OreSat has been provided to stand in place of the actual satellite when integrating COSMOS tools into development.

**Start Mock-OreSat:**

`$` `python3 ./cosmos/mocks/oresat.py`

## COSMOS Install

A docker image has been provided to make the development experience more seamless while allowing COSMOS to operate in the environment it needs. This docker image is based off the official [BallAerospace COSMOS Image](https://hub.docker.com/r/ballaerospace/cosmos) but has been modified to include configurations and settings needed for UniClOGS.

**Install and Run`ms-cosmos` from DockerHub:**

`$` `docker pull dmitrimcguuckin/ms-cosmos`

`$` `docker run --tty --interactive --detach --name cosmos --network=host --ipc=host --env DART_DB=$DART_TEST_DB --env DART_USERNAME=$DART_USERNAME --env DART_PASSWORD=$DART_PASSWORD --env DISPLAY=$DISPLAY --volume $XAUTH:/root/.Xauthority --volume /var/run/postgresql/.s.PGSQL.5432:/var/run/postgresql/.s.PGSQL.5432 dmitrimcguuckin/ms-cosmos`

`$` `docker attach cosmos`

**Note:** *The variables beginning with DART are expected to exist by COSMOS, and can be provided either manually or they can be exported as environment variables in a `.bashrc` file. Either way, they are required in order to forward the details to the container and to COSMOS.*

## PostgreSQL

Visit the [official PostgreSQL website](https://www.postgresql.org/download/) for instructions on how best to install on your system.

## CoSI Daemon

This daemon runs cycles on a preconfigured schedule and polls SpaceTrack for latest Two-Line-Element information and SatnogsDB for latest telemetry information.

**Note:** *Currently, telemetry information is only inserted into the COSMOS packet system and not yet forwarded to the PostgreSQL database.*

**Start the Daemon:**

`$` `cosi/cosid.py start`

**Restart the Daemon:**

`$` `cosi/cosid.py restart`

**Stop the Daemon:**

`$` `cosi/cosid.py stop`

**Useful Links:**

* [`ballcosmos` Infinite Wait Fix](https://github.com/BallAerospace/python-ballcosmos/commit/377552e91ffafea76acedee8cb7ada1abc202898)
* [`ballcosmos` Commands Demonstration](https://github.com/BallAerospace/python-ballcosmos/blob/master/examples/test_json_drb.py)
