FROM python:3.7-alpine
RUN apk add --no-cache build-base zlib-dev tiff-dev openjpeg-dev

COPY ./unit_tests/requirements.txt /requirements_test.txt
COPY ./module_input/requirements.txt /requirements_module_input.txt
COPY ./module_rgba/requirements.txt /requirements_module_rgba.txt
COPY ./module_color/requirements.txt /requirements_module_color.txt

RUN pip install --no-cache-dir -r /requirements_test.txt
RUN pip install --no-cache-dir -r /requirements_module_color.txt
RUN pip install --no-cache-dir -r /requirements_module_input.txt
RUN pip install --no-cache-dir -r /requirements_module_rgba.txt


COPY ./img_processing_common/src /app_common/src
COPY ./img_processing_common/requirements.txt /app_common/
WORKDIR /app_common/src
RUN pip install -e .

COPY ./module_input/src /app_module_input/src
WORKDIR /app_module_input/src
RUN pip install -e .
COPY ./module_rgba/src /app_module_rgba/src
WORKDIR /app_module_rgba/src
RUN pip install -e .

COPY ./module_color/src /app_module_color/src
WORKDIR /app_module_color/src
RUN pip install -e .

COPY ./unit_tests/test_data /tests/test_data
COPY ./unit_tests/tests /tests


WORKDIR /
ENTRYPOINT ["pytest"]
