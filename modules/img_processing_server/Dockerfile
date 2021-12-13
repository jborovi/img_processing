FROM python:3.7-alpine
COPY requirements.txt /
RUN pip3 install --upgrade --no-cache-dir -r /requirements.txt
COPY ./src /app
WORKDIR /app
ENTRYPOINT ["python", "-m", "img_processing_server"]