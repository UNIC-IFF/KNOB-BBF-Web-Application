pipe=bbf-commands
rm -r  $WORKING_DIR/blockchain-benchmarking-framework/$pipe
rm -r  $WORKING_DIR/output.txt
mkfifo ./blockchain-benchmarking-framework/$pipe
touch  ./output.txt
ls
eval "$(cat ./blockchain-benchmarking-framework/$pipe) > ./output.txt" 

