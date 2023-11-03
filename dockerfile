# Use an official Ubuntu as a parent image
FROM python:3.11

# Set environment variables to prevent interactive prompts during installation
# ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=America/New_York

# Update and install necessary packages
RUN apt-get update && apt-get install -y python3-pip python3-dev python3-venv -y

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the entire project directory into the container
COPY app /app

# Expose the port that the Flask app will run on
EXPOSE 5000

# Define the command to run your Flask app
CMD ["python3", "app.py"]
