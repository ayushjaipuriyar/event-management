# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY Pipfile Pipfile.lock /app/

# Install project dependencies
RUN pip install pipenv && pipenv install --system

# Copy the project code to the working directory
COPY . /app/

# Expose the port on which your Django application will run
EXPOSE 8000

# Define the command to run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
