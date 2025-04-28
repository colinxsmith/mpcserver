# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

#Written by COPILOT


# This container is used to control the mpcserver on the laptop from this container

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
# Install mpc and id3v2
# mpc is a command line client for the Music Player Daemon (MPD)    

RUN apt update && apt install -y mpc id3v2

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

#expose the port that mpcserver is running on
EXPOSE 1310

RUN sed -i "s|/home/pi|/app|g" server.py
ENV MPD_HOST=192.168.0.20
ENV MPD_PORT=6600
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "server.py"]
