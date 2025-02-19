FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the dependencies
RUN pip install -r requirements.txt
RUN pip install altair

# Copy the application code
COPY . /app/

# Expose the port
EXPOSE 8501

# Run the command to start the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py"]
