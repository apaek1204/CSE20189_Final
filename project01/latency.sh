#!/bin/sh

#Measure the average latency of spidey.py in single connection vs. forking mode for: direcotyr listings, static files, and CGI scripts

# Latency: (def) How long does it take to do a request
usage(){
	echo "Usage: $0 -p PORT"
}

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

# Use nmap to determine if port is open
OPEN=$(nmap -Pn student00.cse.nd.edu | grep -o "$PORT")


# Do 10 trials
TOTAL=0

for trial in $(seq 10); do 
	if [ ! -z $OPEN ]; then # PORT is open (not an empty string after curling)
		echo "PORT $PORT is open"
		./thor.py -v http://student00.cse.nd.edu:$PORT/ | egrep 'Elapsed time'


	else # PORT is not open
		echo "ERROR: PORT $PORT is not open"
		time=0
		exit
	fi

	echo "Trial $trial average time is $time seconds"
	TOTAL=$(echo "$TOTAL+$time" | bc)
done

AVG_TOTAL=$(echo "$TOTAL/10" | bc)

echo "The average time in a single connection for direcotry listings over 10 trials is $AVG_TOTAL"
