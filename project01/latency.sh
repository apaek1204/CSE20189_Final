#!/bin/sh

#Measure the average latency of spidey.py in single connection vs. forking mode for: direcotyr listings, static files, and CGI scripts

# Latency: (def) How long does it take to do a request
usage(){
	echo "Usage: $0 URL"
}

while getopts h argument; do
	case $argument in 
		h) usage
			exit
			;;
	#	p) PORT=$OPTARG
	#		;;
		*) usage
			exit
			;;
	esac
done

if [ -z $1 ]; then
	usage
else
	URL=$1
fi


./thor.py -r 10 -p 10 -v $URL 2>&1> /dev/null | grep "Average" | awk 'BEGIN{FS="|"} {print $2}' | awk 'BEGIN{FS=":"}{print $2}' | awk 'BEGIN{FS=" "}{sum += $1; n++}END{ if (n>0) print sum/n}'

