# Watercolor, an batch image upscaling service.
[Read the Paper](https://drive.google.com/file/d/1PzlfL3u_YCR4NGQu_GzBmSFIPpEi4upc/view?usp=sharing)
## Usage

### Deploying to minikube

First, ensure `minikube` is running:

`minikube start --driver=docker`

Then, to deploy the backend to the cluster, run:

`./backend/deploy.sh`

Consult the README in the `backend/` folder for more information.

### Individual containers

You can also build and run the individual docker images that make up
Watercolor without a Kubernetes cluster. 

Building:

`docker build ./backend/api -t wtc-api`
`docker build ./backend/processing -t wtc-process`

Running:
`docker run --publish <port>:5000 --name watercolor-api wtc-api`
`docker run --publish <port>:32017 --name watecolor-processing wtc-process`

Consult the README in the `backend/` folder for more information.
