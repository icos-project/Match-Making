# Use the base image of Ubuntu with a specific tag instead of "latest"
FROM ubuntu:20.04

# Update the package index and install Python3 and pip
RUN apt-get update -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Create the application directory
WORKDIR /app
COPY requirements.txt .

# Install necessary libraries with specific versions
RUN pip3 install -r requirements.txt

#RUN pip3 install --no-cache-dir \
#    fastapi==0.103.2 \
#    uvicorn==0.13.4 \
#    httpx==0.25.0 \
#    pyyaml==5.3.1 \
#    requests==2.31.0


# Copy files from the local folder to the image at /app
COPY core /app/core
COPY api /app/api
COPY tools /app/tools
COPY unittests /app/unittests

# Expose port 8000 for the application
EXPOSE 8000

WORKDIR /app/api
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/api"
# Command to run the application
CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0"]
