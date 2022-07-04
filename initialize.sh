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
    if [ -z "$(ls -A $WORKING_DIR/blockchain-benchmarking-framework )" ]; then
        git clone "https://github.com/UNIC-IFF/blockchain-benchmarking-framework.git" 
        git -C $WORKING_DIR/blockchain-benchmarking-framework submodule update --init --recursive 
    else
        git -C $WORKING_DIR/blockchain-benchmarking-framework submodule update
    fi
	
else
    echo "Error: Directory $WORKING_DIR/blockchain-benchmarking-framework does not exists."
        git clone "https://github.com/UNIC-IFF/blockchain-benchmarking-framework.git"
        git -C $WORKING_DIR/blockchain-benchmarking-framework submodule update --init --recursive
fi

echo "Creating pipe if not exist"
pipe=bbf-commands



if [[ ! -p "$WORKING_DIR/blockchain-benchmarking-framework/$pipe" ]]; then
    mkfifo $WORKING_DIR/blockchain-benchmarking-framework/$pipe
	echo "Pipe created"
else
    echo "Pipe already exists"
fi

echo "Make the pipe listen forever in background..."
while true; do 
    eval "$(cat $WORKING_DIR/blockchain-benchmarking-framework/$pipe) &> $WORKING_DIR/output.txt" ; 
done 






