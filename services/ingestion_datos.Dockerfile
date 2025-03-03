
# Use the official Python base image
FROM python:3.10.7-slim

# Set the working directory inside the container
WORKDIR /ingestion_datos

# Copy the requirements file to the working directory
COPY ingestion_datos-requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r ingestion_datos-requirements.txt

# Copy the source code to the working directory
COPY ./ ./

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app
CMD ["uvicorn", "ingestion_datos.main:app", "--host=0.0.0.0", "--port=8000"]
