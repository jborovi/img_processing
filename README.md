# Image processing modules

This project process pictures on input, gets their average color and stores it in folder

## Prerequisities
- python3
- docker
- docker-compose


## Quickstart

from project root

```docker-compose -f docker-compose.prod.yml  -f docker-compose.yml up --build```

you can upload file by [upload_image](./scripts/upload_image.py)
```
./scripts/upload_image.py {path to your file}
```

alternatively by

```commandline
docker cp {path to your file}  img_processing_module_input_1:/tmp/images/input/{your filename}
```

## unit-tests

```docker-compose -f docker-compose-unit_test.yml up --build```

## project modules
- [module_input](./modules/module_input)

  process input file and send message to [module_rgba](./modules/module_rgba)
- [module_rgba](./modules/module_rgba)

  Receive messages from [module_input](./modules/module_input)

  gets average rgba value from the picture and sends rgba message to [module_color](./modules/module_color)
- [module_color](./modules/module_color)

  Receive messages from [module_rgba](./modules/module_rgba) decides the color name and stores picture into the color folder by color name.

- [img_processing_common (shared lib)](./modules/img_processing_common)

  Code which is shared across modules

## extra module
- [img_processing_server](./modules/img_processing_server)

  Provides interface to upload picture into system, or optionally extend for user interface
  By default it listens on port *8081*, you can change port by setting *SERVER_HTTP_PORT* at  [.env](.env) file

Project uses [redis](https://redis.io/) as for communication between modules
and shared volume between containers

## tests

- [unit_tests](./modules/unit_tests)

  covers following [modules](./modules/unit_tests/tests)

  i tested for following formats
  - jpeg
  - jpeg200
  - bmp
  - png
  - tif
  - dds

project is logging via driver: json-file
you should see output in your console
example of successful result

```INFO:img_processing_common.logger:moved {'d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5'} to yellow```
