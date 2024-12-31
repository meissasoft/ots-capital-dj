# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

COPY ./docker/entrypoint.sh entrypoint.sh.raw
RUN sed 's/\r$//' entrypoint.sh.raw > entrypoint.sh \
    && rm entrypoint.sh.raw

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]

# Run the Django server
CMD ["serve", "--bind", "0.0.0.0:8000"]
