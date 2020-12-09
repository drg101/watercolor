#! /bin/bash

PODS_API=`kubectl get pods | grep -oi "wtc-api-[0-9a-z]\+-[0-9a-z]\+"`
PODS_BACKEND=`kubectl get pods | grep -oi "wtc-process-[0-9a-z]\+-[0-9a-z]\+"`

echo "Showing API logs:"
echo "---------------------"
for POD in $PODS_API; do
    echo "Pod $POD:"
    kubectl logs $POD
done
echo "---------------------"
echo "End of API logs."
echo ""
echo "Showing backend logs:"
echo "----------------------"
for POD in $PODS_BACKEND; do
    echo "Pod $POD":
    kubectl logs $POD
done
echo "---------------------"
echo "End of backend logs."

