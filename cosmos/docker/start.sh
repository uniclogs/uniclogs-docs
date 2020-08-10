#!/usr/bin/env bash

function action() {
  echo -e "\n\n---\nSTARTING ACTION: : $1\n---\n"
  $1
}

action "bundle exec rake db:schema:load" && action "bundle exec rake db:seed" &
action "ruby tools/Dart" &
action "ruby tools/CmdTlmServer --no-gui" &

echo -e "Finished starting all of the services!"

echo -e "Will spin forever now..."

while [[ 1 ]]; do
  echo -e "[$(date)]: Spinning..."
  sleep 1
done
