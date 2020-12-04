#! /bin/bash

source ./.script_utils

#  
# backend/deploy.sh 
#
# Builds & deploys the watercolor backend to a minikube cluster.
# Minikube must already be running!
# (try `sudo minikube start --driver=docker`)
# The excuting user must either be in the "docker" group (preferred)
# or have root permissions (bad, please don't).
#

TARGETS=('wtc-api' 'wtc-process')

find_service()    { kubectl get svc $1 &> /dev/null; }
destroy_service() { kubectl delete svc $1; }
destroy_depl()    { kubectl delete deployment $1; }
create_service()  { kubectl apply -f $1_service.yml; }
create_depl()     { kubectl apply -f $1_deployment.yml; }

BUILD_CMD="./build.sh"

OPT_KILLONLY=

while getopts 'k' OPT
do
    case $OPT in
    k) OPT_KILLONLY=true ;;
    esac
done

predeploy() {
    if [[ $MINIKUBE_ACTIVE_DOCKERD != "minikube" ]]; then
        echo -e "$INF_PREFIX Local image deployment was not detected: setting environment variables..."
	eval $(minikube -p minikube docker-env)
    fi
}

deploy() {
    if [[ -z $OPT_KILLONLY ]]; then
        exec_and_test "$BUILD_CMD" "Couldn't deploy: failed to build one or more containers.";
    fi

    echo -e "$INF_PREFIX Killing existing services..."
    for target in "${TARGETS[@]}"; do
        if find_service $target; then
	    destroy_service $target
	    destroy_depl $target
	fi 
    done

    if [[ -n $OPT_KILLONLY ]]; then
        exit 0
    fi

    echo -e "$INF_PREFIX Creating services..."
    for target in "${TARGETS[@]}"; do
        exec_and_test "create_service $target" "Failed to create '$target' service."
    done

    echo -e "$INF_PREFIX Making deployments..."
    for target in "${TARGETS[@]}"; do
        exec_and_test "create_depl $target" "Failed to deploy '$target'."
    done
}

predeploy
deploy
exit 0

