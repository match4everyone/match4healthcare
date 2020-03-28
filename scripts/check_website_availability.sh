#!/usr/bin/env bash

# ======================================================================================
# title			:  check_website_basic.sh
# description	:  Checks if the website is up and can be served as well as
#				   whether Django throws an error while serving
# author       	:  Kevin Yuan
# date			:  28.03.2020
# version		:  1.0
# notes			:  This script is called by travis but should work locally too
# ======================================================================================

# Setting some colors
red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# Return variable
failed=False

# Execute command and print status
function test() {
	printf "${1}:\t"
	eval "$2" &> /dev/null
	if [[ $? -eq 0 ]]; then
		printf "${grn}Pass\n${end}"
	else
		failed=True
		printf "${red}Failed\n${end}"
	fi
}


function check_website_up() {
	if [[ ! $(curl -o /dev/null --silent --head --write-out '%{http_code}\n' localhost:8000) -eq 200 ]]; then 
		return 1
	fi
}

function check_error_log_empty() {
	if [  -s backend/run/match4healthcare.log ]; then
		return 1
	fi
}

test "Website reachable" "check_website_up"
test "Error log empty" "check_error_log_empty"

# If everything went well we exit with zero, else one
if [[ $failed -eq "True" ]]; then
	exit 1
else 
	exit 0
fi