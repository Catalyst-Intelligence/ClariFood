# Using the official lightweight Python image as a foundation
FROM python:3.13.5-slim

# Setup the operational directory inside the virtual container
WORKDIR /app

# Linux system configuration sequence
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libzbar0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements map
COPY requirements.txt ./

# install dependancies
RUN pip3 install -r requirements.txt

# Copy main application file directly from your root folder
COPY app.py ./

# Tell container to open the port the app listens to
EXPOSE 8501

# Health monitoring
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Boot execution
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
