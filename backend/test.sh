#! /bin/bash

source ./.script_utils

#
# backend/test.sh
# Convenience script for testing applications deployed in Watercolor.
# You must provide at least a request type, probably GET or POST.
# You can then specify JSON to be sent in the second parameter.
# A third parameter is also possible that accepts a MIME type, in case
# you want to send something other than JSON.
#
# Examples:
# ./test.sh GET
# ./test.sh POST '{"id":3,images:["my_cool_image"]}'
#

if [[ $# -ne 3 && $# -ne 2 && $# -ne 1 ]]; then
    echo -e "$ERR_PREFIX wrong number of aruguments."
    echo -e "$ERR_PREFIX (Got $#, expected at least 1, max 3.)"
    echo "Usage: $0 <request_type> [json_body] [content_type]"
    exit 1
fi

exec_and_test "kubectl get svc wtc-api" "Could not find the wtc-api service." >> /dev/null

# Thanks to Joe for discovering this cracked command from deep within
# the Kubernetes tutorials
NODE_PORT=$(kubectl get services/wtc-api -o go-template='{{(index .spec.ports 0).nodePort}}')
TARGET_IP=$(minikube ip):$NODE_PORT

CONTENT_TYPE=
if [[ -n $3 ]]; then
    CONTENT_TYPE=$3
else
    CONTENT_TYPE="application/json"
fi

CURL_TEST_CMD=
if [[ -z $2 ]]; then
    CURL_TEST_CMD="curl -X $1 $TARGET_IP"
else 
    CURL_TEST_CMD="curl -X $1 -H Content-Type:"${CONTENT_TYPE}" -d "${2}" ${TARGET_IP}"
fi

run_test() {
    if ! exec_and_test "$CURL_TEST_CMD" "Failed to run the test command."; then
        echo -e "$INF_PREFIX Pay attention to spaces in your input."
	echo -e "$INF_PREFIX Make sure that your content payload is surrounded by single quotes (\')."
    fi
}

run_test
exit 0

