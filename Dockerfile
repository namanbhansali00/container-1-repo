FROM python:3.8-slim

WORKDIR /app

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (if needed)
# ENV MY_ENV_VAR=value

# Expose the port on which Flask app will run
EXPOSE 80

# Run the Flask application
CMD ["python", "app.py"]
