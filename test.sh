#!/bin/sh

echo "--- Building docker image ---"
docker build -t pytorch-docker .
docker images

echo "--- Run the image as a container ---"
docker run -d -p 5000:5000 --name http-server pytorch-docker
docker ps

echo "--- Check whether server is running... ---"
sleep 10
curl localhost:5000

echo " "
echo "--- Query the server using images ---"
curl -F "file=@chicken.jpeg" http://127.0.0.1:5000/upload
echo " "
curl -F "file=@puppy.jpeg" http://127.0.0.1:5000/upload
echo " "
curl -F "file=@pig.jpeg" http://127.0.0.1:5000/upload
echo " "
curl -F "file=@cat.jpeg" http://127.0.0.1:5000/upload

echo " "
echo "--- Inference is done... ---"
docker stop http-server