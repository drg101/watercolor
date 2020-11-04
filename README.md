# Watercolor, an image processing service.

## Usage

First, build the image. Navigate to the root of this repository (the same folder
this README is in!) and execute (with root permissions):
```
# docker build -t watercolor .
```

Wait for it to complete. It may take a while.

Once done, run the image. Choose a port to listen on for requests, then execute:

```
# docker run --publish <port>:5000 --name watercolor watercolor:latest
```

The server will then be running.


**For example:**

```
# docker run --publish 8080:5000 --name watercolor watercolor:latest
```

Will start a docker container named **watercolor** with a server which responds to requests made to **localhost:8080**

## Testing
to test the server(while the docker container is running) with a simple curl request try 
```
# curl -X GET -H "Content-Type: application/json" -d '{"test":"obj"}' localhost:<port>
```
which should print `{"data": "you ran a GET request", "args": {"test": "obj"}}`
