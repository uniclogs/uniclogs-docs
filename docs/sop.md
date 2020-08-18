# Mission Server SOP
Installing the mission server on a server running Arch Linux.

## Deploy / Install / Update
- `$ sudo git clone https://github.com/oresat /opt`
- Postgresql - Follow arch [postgres wiki]
    - `$ yay -S postgres`
    - `$ sudo systemctl start postgres`
    - `$ sudo systemctl enable postgres`
    - `$ sudo -iu postgres`
    - `$ initdb -D /var/lib/postgres/data`
    - `$ createuser --interactive`
    - `$ createdb cosmos`
    - `$ psql -d cosmos`
    - Run all sql scripts in uniclogs-software/scripts
    - Configure additional super-users for RADS and ULTRA that have all access to tables/functions/sequences on the cosmos database.
- Add environment variable
    - Put all these in /etc/environment
    ```
    export DART_HOST="localhost"
    export DART_PORT="5432"
    export DART_DB="cosmos"
    export DART_USERNAME="root"
    export DART_PASSWORD="password here"
    export COSI_USER_NAME="root"
    export COSI_PASSWORD="password here"
    export ULTRA_USER_NAME="root"
    export ULTRA_PASSWORD="password here"
    export RADS_USERNAME="root"
    export RADS_PASSWORD="password here"
    export COSMOS_USERPATH="/tmp/userpath.txt"
    ```
- Docker / COSMOS
    - `$ yay -S docker`
    - `$ docker pull psaspdx/cosmos`
    - `$ docker run  --tty --detach --name command-telemetry-server --network=host --ipc=host --env DART_DB=cosmos --env DART_USERNAME=psas  --env DART_PASSWORD=<postgres password> --volume $PG_SOCKET:$PG_SOCKET psaspdx/cosmos`
- Apache
    - Configure subdomain routing to ULTRA
- Install python and pip on Arch
    - `$ yay -S python pip`
- Install pass calculator
    - `$ sudo pip install pass-calculator`
- Install RADS
    - `$ sudo pip install rads?????`
- Install ULTRA
    - `$ sudo pip install -r /opt/uniclogs-software/ultra/requirements `
    - `$ sudo cp /opt/uniclogs-software/ultra/ultrad.service /lib/systemd/system`
    - `$ sudo systemctl reload`
    - `$ sudo systemctl start ultrad`
    - `$ sudo systemctl enable ultrad`
- Install CoSI
    - `$ sudo pip install -r /opt/uniclogs-software/cosi/requirements `
    - `$ sudo cp /opt/uniclogs-software/cosi/cosid.service /lib/systemd/system`
    - `$ sudo systemctl reload`
    - `$ sudo systemctl start cosid`
    - `$ sudo systemctl enable cosid`

## Run
- `$ rads` to launch rads

## Uninstall 
- Unplug the server and throw it in the trash


[postgres wiki]:https://wiki.archlinux.org/index.php/PostgreSQL
