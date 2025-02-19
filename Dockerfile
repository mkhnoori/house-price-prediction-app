FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8501

# Create a non-root user
RUN useradd -m -s /bin/bash app_user

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Train the model and generate necessary files
RUN cd models && python train_model.py

# Set ownership to non-root user
RUN chown -R app_user:app_user /app

# Switch to non-root user
USER app_user

# Expose the port
EXPOSE $PORT

# Set healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
CMD ["streamlit", "run", "--server.port", "8501", "--server.address", "0.0.0.0", "main.py"]
