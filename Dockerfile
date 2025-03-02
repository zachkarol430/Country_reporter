# Use an official Python runtime as a parent image
FROM python:3.10-slim


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --verbose


# Make port 8000 available to the world outside this container (if needed)
EXPOSE 8000

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run the app when the container launches
CMD ["python", "api.py"]