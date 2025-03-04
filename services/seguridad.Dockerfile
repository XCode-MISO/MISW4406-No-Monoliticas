
# Use the official Python base image
FROM python:3.10.7-slim

# Set the working directory inside the container
WORKDIR /seguridad

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the working directory
COPY ./seguridad .

# Expose the port on which the Flask app will run
EXPOSE 5001

# Run the Flask app

CMD ["flask", "--app", "api",  "--debug", "run", "--host=0.0.0.0"]
