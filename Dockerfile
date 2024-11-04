# Use the official Python image from the Docker Hub
FROM python:3.8.20-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy the rest of the application code into the container
COPY . .

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app/api/app.py"]