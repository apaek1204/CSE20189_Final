#!/bin/sh

#measure the avg throughput of spidey.py in single connection vs forking mode for: small static files (1KB), medium static files (1MB), and large static files (1GB) 

usage(){
  echo "Usage: $0 -p PORT"
}
#arguments
while getopts hp: argument; do
  case $argument in
    h) usage
      ;;
    p) PORT=$OPTARG
      ;;
    *) usage
      ;;
  esac
done

#100 trials
TOTAL=0
TIME=0

for giga in $(seq 1); do
  ./thor.py -p 1 -r 1 -v http://student00.cse.nd.edu:$PORT/www/throughput/gigabyte 2>&1 > /dev/null | grep "Average" | awk -F" " '{print $8}' >> throughput_giga_test2.txt
done
