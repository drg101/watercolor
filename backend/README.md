Watercolor's backend. Uses k8 and docker.

# Deployment

## Structure

Watercolor's backend is divided into two parts:
* **The API**, a flask server that listens for TCP HTTP requests on (by
  default) port 5000. This is what clients must send GET/POST requests to.
* **The Processing backend**, another server that listens for raw TCP on (by
  default) port 32017. The API passes images to this backend to do the actual
  processing, and the backend sends them back to the API once it is finished
  to be passed back to the client.

Both components are built and deployed as docker containers. The script
`./build.sh` can be used to build both locally. The API container is called
`wtc-api` and the processing backend container is called `wtc-process`. They
can be run individually as normal docker containers:

`docker run --publish 5000:5000 --name watercolor-api wtc-api #runs the api, exposing port 5000`
`docker run --publish 32017:32017 --name watercolor-processing wtc-process #runs the processing server, exposing port 32017`

(`./build.sh` accepts a `-n` flag to avoid using the Docker cache. This is
sometimes necessary when making changes to the Dockerfile or the files copied
into the container. If in doubt, provide it.)

Watercolor is intended to be run under Kubernetes. A cluster running
Watercolor contains a single API container and any number of backend
containers. The backend containers are tied together by a Service, providing
a single IP for which the API can pass images to for processing. The API also
sits behind a Service, although it is not necessarily used by the backend.

The API and each backend container are in a separate Pod. The Services are
used to provide inter-Pod communication - the API knows the IP of the backend
Service through an environment variable, and passes requests to this IP, where
Kubernetes then handles load balancing to each of the backend containers. DNS
is not used to resolve the Service IPs - they are used directly through
enrivonrment variables.

By default, the cluster provisions three backend containers and one API
container. More than one API container is not supported and may explode
horribly. These numbers can be changed in the corresponding `*_deployment.yml`
files, by changing the `replicas` fields.

The entire deployment process can be invoked with the `./deploy.sh` script.
This will build the containers, kill any active deployments and Services,
then re-create the Services and apply the deployments. If necessary, it will
also set environment variables that tell `minikube` to use local docker images
instead of remote ones. This is necessary since we currently do not have the
images on Dockerhub, which is where it would look for them by default.

To destroy the current deployment without making a new one, you can invoke
`./deploy.sh` with the `-k` flag.

Before running `./deploy.sh`, make sure that `minikube` is started:

`minikube start --driver=docker`

# File Structure 
	api/
		__init__.py
		app.py          # this file contains your app and routes
		Dockerfile      # The API dockerfile
		resources/
			__init__.py
			r1.py #resource 
		common/
			__init__.py
			util.py #random utility file
	build.sh       # Builds the Docker images locally
        deploy.sh      # Deploys watercolor to a local minikube cluster
        processing/
		Dockerfile           # The backend dockerfile
		environment.yml      # A description of the backend's dependencies for Miniconda
		process.py           # The backend itself
	.script_utils  
        wtc-api_deployment.yml       # Deployment spec for the API
        wtc-api_service.yml          # Service spec for the API, currently unusued
        wtc-process_deployment.yml   # Deployment spec for the backend
        wtc-process_service.yml      # Service spec for the backend


