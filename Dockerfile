# Base Python Image
FROM python:3.9.6

# Set the working directory
WORKDIR /code

# Copy the requirements file which contains dependencies to run the webservice
COPY ./requirements.txt /code/requirements.txt

# Install dependencies from requirements.txt
RUN pip install -r /code/requirements.txt

# Copy source code files
COPY ./app /code/app

# Command to run the app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]