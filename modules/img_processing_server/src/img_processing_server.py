"""
http interface for project
"""


import asyncio
import base64
import io
import json
import logging
import os
from hashlib import sha256

from aiohttp import web
from PIL import Image, UnidentifiedImageError

DATA_SOURCE = os.path.join(
    os.getenv("SHARED_VOLUME", "/tmp/images"),
    os.getenv("DIR_INPUT", "input"),
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def upload_image(request):
    if not request.body_exists:
        return web.Response(
            status=400, body=bytes(json.dumps({"error": "Not image"}), "utf-8")
        )
    im_b64 = await request.json()
    img_bytes = base64.b64decode(im_b64["image"].encode("utf-8"))
    sha_256 = sha256()
    sha_256.update(img_bytes)
    # convert bytes data to PIL Image object
    status = 500
    response_body = bytes(json.dumps({"error:": "unknown"}), "utf-8")
    try:
        Image.open(io.BytesIO(img_bytes))
        status = 200
        response_body = bytes(
            json.dumps({"image_sha": str(sha_256.hexdigest())}), "utf-8"
        )
    except UnidentifiedImageError:
        response_body = bytes(json.dumps({"error": "Not image"}), "utf-8")
        status = 400
    try:
        os.mkdir(DATA_SOURCE)
    except FileExistsError:
        pass
    with open(os.path.join(DATA_SOURCE, str(sha_256)), "wb") as file:
        file.write(img_bytes)

    return web.Response(status=status, body=response_body)


async def handle_upload_image(request):
    return await upload_image(request)


if __name__ == "__main__":
    app = web.Application(client_max_size=50000000)
    app.router.add_route("POST", "/image", handle_upload_image)
    loop = asyncio.get_event_loop()
    f = loop.create_server(app.make_handler(), "0.0.0.0", 8080)
    srv = loop.run_until_complete(f)
    print("serving on", srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
