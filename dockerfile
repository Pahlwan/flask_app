# linux packages
FROM ubuntu:20.04

# Install python3.9
RUN apt-get update && apt-get install -y python3.9 

# Install pip3
RUN apt-get install -y python3-pip

# Install mysql
RUN apt-get install -y libmysqlclient-dev

# Set the working directory to /app
WORKDIR /flask_app

# Copy the current directory contents into the container at /app
COPY . /flask_app

# Upgrade pip
RUN pip3 install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run app.py when the container launches
CMD ["flask", "run"]

