#!/bin/bash

DEFAULT_ENVFILE="$(dirname $0)/defaults.env"
ENVFILE=${ENVFILE:-"$DEFAULT_ENVFILE"}

source $ENVFILE

while true
do 
    git pull
	git submodule update
	docker exec bbf-gui-apis sh -c "gulp &"
    sleep 43000
done
