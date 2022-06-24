#!/bin/bash

DEFAULT_ENVFILE="$(dirname $0)/defaults.env"
ENVFILE=${ENVFILE:-"$DEFAULT_ENVFILE"}
INIT_PATH=WORKING_DIR=${WORKING_DIR:-$(realpath ./blockchain-benchmarking-framework/bbf-commands)}

source $ENVFILE


docker-compose up -d --build


if [ -d "$WORKING_DIR/blockchain-benchmarking-framework" ] 
then
    echo "Directory $WORKING_DIR/blockchain-benchmarking-framework exists." 
	echo "Requesting any updates..." 
	git -C $WORKING_DIR/blockchain-benchmarking-framework submodule update
	
else
    echo "Error: Directory $WORKING_DIR/blockchain-benchmarking-framework does not exists."
	git clone "https://github.com/UNIC-IFF/blockchain-benchmarking-framework.git"
	git -C $WORKING_DIR/blockchain-benchmarking-framework submodule update --init --recursive
fi

echo "Creating pipe if not exist"
pipe=bbf-commands


if [[ ! -p $pipe ]]; 
then
    mkfifo $pipe
	echo "Pipe created"
else
    echo "Pipe already exists"
fi

echo "Make the pipe listen forever..."
while true; do 
    eval "$(cat ./$pipe)"; 
done






