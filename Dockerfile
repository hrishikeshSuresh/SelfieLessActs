# Use an official Python runtime as a parent image
FROM alpine:3.7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apk add --update \
    python3 \
    python-dev \
    py-pip \
    build-base \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
<<<<<<< HEAD
CMD ["python3", "server.py"]
#CMD flask run --host 0.0.0.0
=======
CMD ["python", "server.py"]
>>>>>>> 4ff5a4effbe1b311c167278f9da223535ccd1f7a

