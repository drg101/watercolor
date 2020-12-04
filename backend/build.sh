#! /bin/bash

source ./.script_utils

OPT_CACHE=

while getopts 'n' OPT
do
    case $OPT in
    n) OPT_CACHE="--no-cache"
       echo -e "$INF_PREFIX Buliding without cache."
       ;;
    esac
done

API_BUILD_CMD="docker build $OPT_CACHE ./api/ -t wtc-api"
BACKEND_BUILD_CMD="docker build $OPT_CACHE ./processing/ -t wtc-process"

build() {
    echo -e "$INF_PREFIX Building the Watercolor backend."
    echo -e "$INF_PREFIX Building api container..."
    exec_and_test "$API_BUILD_CMD" "Failed to build the api container"
    exec_and_test "$BACKEND_BUILD_CMD" "Failed to build the backend container"
    echo -e "$SUC_PREFIX Built all containers."
}

build

exit 0
