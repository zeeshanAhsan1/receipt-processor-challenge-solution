# receipt-processor-challenge-solution

Webservice for the receipt-processor-challenge for fetch-rewards based in Python (FastAPI)

## Pre-requisites

1. Make sure docker is installed on the machine.

2. Make sure port '8004' is free on the machine. If it is not, then modify the port of the container in the 4th step in 'Installation' and use webservice accordingly.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/zeeshanAhsan1/receipt-processor-challenge-solution.git

   ```

2. Make sure you are in the base directory of the project. ('receipt-processor-challenge-solution')

3. In your docker environment, build an image -> This takes care of environment and all dependencies setup for the project.

   ```sh
   docker build -t receipt-processor-image:1.0 .

   ```

4. Check if the docker image is successfully built.

   ```sh
   docker images

   ```

5. Run a container using this image.

   ```sh
   docker run -d --name receipt-processor-container -p 8004:80 receipt-processor-image:1.0

   ```

6. Check if the container is up and running.

   ```sh
   docker ps

   ```

7. Check if the webservice has started inside the container using logs of the container.

   ```sh
   docker logs receipt-processor-container

   ```

## Usage

1. The application can be used on your local machine at : (http://localhost:8004/)

2. The application doesn't have a UI. To try the app, you can goto - (http://localhost:8004/docs). This is the Swagger Docs page.

3. In then POST and GET methods, goto - 'Try it out' option.
