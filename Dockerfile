# Use official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary alembic

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
