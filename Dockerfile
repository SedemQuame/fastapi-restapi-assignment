# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables (if needed)
ENV MONGO_DB_NAME=
ENV MONGO_URI=
ENV TWILIO_ACCOUNT_SID=
ENV TWILIO_AUTH_TOKEN=

# Run the application
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "8000"]

