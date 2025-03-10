
# Use the official Python base image
FROM python:3.10.7-slim

# Set the working directory inside the container
WORKDIR /bff

# Copy the requirements file to the working directory
COPY ingestion_datos-requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r ingestion_datos-requirements.txt

# Copy the source code to the working directory
COPY ./ ./

# Expose the port on which the Flask app will run
EXPOSE 8000

# Run the Flask app
CMD ["uvicorn", "bff.main:app", "--port=8000", "--host", "0.0.0.0"]
