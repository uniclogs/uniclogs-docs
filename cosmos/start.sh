#!/usr/bin/env bash

DELAY_TIME=60

function spin() {
  if [[ $? == 0 ]]; then
    echo -e "All processed daemonized, will spin forever now..."

    while [[ 1 ]]; do
      echo -e "[$(date)]: This is your $DELAY_TIME-second checkin... Yep... still alive."
      sleep $DELAY_TIME
    done
  else
    echo -e "A process failed to daemonize, exiting start script!"
  fi

}

bundle exec rake db:schema:load
bundle exec rake db:seed

ruby ruby tools/CmdTlmServer --production --no-gui & spin
