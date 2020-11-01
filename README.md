Watercolor, a image processing service.

# Building and running with Docker

First, build the image. Navigate to the root of this repository (the same folder
this README is in!) and execute (with root permissions):
```
# docker build --tag watercolor:0.1 .
```

Wait for it to complete. It may take a while.

Once done, run the image. Choose a port to listen on for requests, then execute:

```
# docker run --publish <port>:5000 --name watercolor watercolor:0.1
```

The server will then be running.

