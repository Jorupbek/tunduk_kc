# Pull official base image 
FROM python:3.11-slim

# Set working directory
WORKDIR /app
COPY . /app/

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc python3-dev

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry
# Install dependencies
RUN poetry install

# Copy entrypoint.sh
COPY ./compose/back/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]