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
    && python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && pip install --upgrade pip \
    && pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV TEAM_ID CC_139_159_158_713

# Run app.py when the container launches
CMD ["python3", "user_management_ms.py"]
#CMD flask run --host 0.0.0.0

