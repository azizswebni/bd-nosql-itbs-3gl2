# Base Image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "run.py"]