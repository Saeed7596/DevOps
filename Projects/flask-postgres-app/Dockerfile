FROM python:3.10-slim

# Install dependencies
RUN pip install Flask psycopg2-binary

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py /app
COPY templates/ /app/templates/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
