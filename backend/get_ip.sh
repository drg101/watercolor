#! /bin/bash

NODE_PORT=$(kubectl get services/wtc-api -o go-template='{{(index .spec.ports 0).nodePort}}')
TARGET_IP=$(minikube ip):$NODE_PORT

echo "http://$TARGET_IP/"
