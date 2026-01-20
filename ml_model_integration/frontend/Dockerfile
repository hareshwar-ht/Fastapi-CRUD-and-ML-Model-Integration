# Base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "frontend_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]