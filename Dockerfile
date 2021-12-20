# syntax=docker/dockerfile:1

#Using the Python 3.7 image as the launching point
ARG BASE_CONTAINER=python:3.7
From $BASE_CONTAINER

#Creating the working directory
WORKDIR /app

#Installing the required dependencies
COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

#Taking all the files located in the current directory and copies them into the image
COPY . .

#Exposing the port 5000 from container
EXPOSE 5000

#Starting the python application and make the application externally visible
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

