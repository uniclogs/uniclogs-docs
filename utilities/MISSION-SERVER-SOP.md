# Mission Server SOP
Installing the mission server on a server running Arch Linux.

## Deploy / Install / Update
- `$ sudo git clone https://github.com/oresat/uniclogs-software /opt`
- Postgresql - Follow arch [postgres wiki]
    - `$ yay -S postgresql`
    - `$ sudo systemctl start postgresql`
    - `$ sudo systemctl enable postgresql`
    - `$ sudo -iu postgres`
    - `$ initdb -D /var/lib/postgres/data`
    - `$ createuser --interactive`
    - `$ createdb cosmos`
    - `$ psql -d cosmos`
    - Run all sql scripts in `uniclogs-software/db_schemas`
    - Configure additional super-users for RADS and ULTRA that have all access to tables/functions/sequences on the cosmos database.
- Add environment variable
    - Put all these in /etc/environment
    ```
    DART_HOST="localhost"
    DART_PORT="5432"
    DART_DB="cosmos"
    DART_USERNAME="username here"
    DART_PASSWORD="password here"
    COSI_USER_NAME="cosi"
    COSI_PASSWORD="password here"
    ULTRA_USER_NAME="ultra"
    ULTRA_PASSWORD="password here"
    RADS_USERNAME="rads"
    RADS_PASSWORD="password here"
    COSMOS_USERPATH="/tmp/userpath.txt"
    SATNOGS_TOKEN="token here"
    SPACETRACK_USERNAME="username here"
    SPACETRACK_PASSWORD="password here"
    ```
- Docker / COSMOS
    - `$ yay -S docker`
    - `$ docker pull psaspdx/cosmos`
    - `$ docker run --tty --detach --name command-telemetry-server --network=host --ipc=host --env DART_DB=$DART_DB --env DART_USERNAME=$DART_USERNAME --env DART_PASSWORD=$DART_PORT --volume $PG_SOCKET:$PG_SOCKET psaspdx/cosmos`
- Apache
    - Configure subdomain routing to ULTRA
- Install python and pip on Arch
    - `$ yay -S python pip`
- Install pass calculator
    - `$ sudo pip install pass-calculator`
- Install RADS
    - `$ sudo pip install uniclogs-rads`
- Install ULTRA
    - `$ sudo pip install -r /opt/uniclogs-software/ultra/requirements`
    - `$ sudo cp /opt/uniclogs-software/ultra/ultrad.service /lib/systemd/system`
    - `$ sudo systemctl daemon-reload`
    - `$ sudo systemctl start ultrad`
    - `$ sudo systemctl enable ultrad`
- Install CoSI
    - `$ sudo pip install -r /opt/uniclogs-software/cosi/requirements`
    - `$ sudo cp /opt/uniclogs-software/cosi/cosid.service /lib/systemd/system`
    - `$ sudo systemctl daemon-reload`
    - `$ sudo systemctl start cosid`
    - `$ sudo systemctl enable cosid`

## Run
- `$ rads` to launch rads

## Uninstall
- Unplug the server and throw it in the trash


[postgres wiki]:https://wiki.archlinux.org/index.php/PostgreSQL
