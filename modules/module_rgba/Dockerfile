FROM python:3.7-alpine as app_common
RUN apk add --no-cache build-base zlib-dev tiff-dev openjpeg-dev
COPY ./img_processing_common/src /app_common
COPY ./img_processing_common/requirements.txt /app_common/
RUN pip install --upgrade --no-cache-dir -r /app_common/requirements.txt
WORKDIR /app_common
RUN python setup.py install
FROM app_common as module_rgba
COPY ./module_rgba/requirements.txt /app/requirements.txt
RUN pip install --upgrade --no-cache-dir -r /app/requirements.txt
COPY ./module_rgba/src /app
WORKDIR /app
CMD ["python", "-m", "module_rgba.main"]
