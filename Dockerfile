# Base image -> https://github.com/runpod/containers/blob/main/official-templates/base/Dockerfile
# DockerHub -> https://hub.docker.com/r/runpod/base/tags
FROM downloads.unstructured.io/unstructured-io/unstructured-api:latest

# Switch to the root user to install system dependencies
USER root

# Install System Dependencies
RUN apk add --no-cache supervisor && \
    pip install setuptools

# Switch back to the non-root user
USER ${NB_USER}

# Python dependencies
COPY requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Set up supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT ["python3.11", "-u", "./handler.py"]
#CMD python3.11 -u /handler.py
