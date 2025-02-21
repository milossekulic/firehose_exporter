FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory contents into the container at /usr/src/app/app
COPY app/ ./app

# BEFORE STARTING CONTAINER FIRST CREATE CONFIG.JSON IN THE ROOT OF THE DIRECTORY
# Copy config.json into the container at /usr/src/app/
COPY config.json .

CMD ["python", "-m", "app.main"]