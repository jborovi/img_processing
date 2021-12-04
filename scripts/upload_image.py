#!/usr/bin/env python3

import argparse
import base64
import json

import requests

URL = "http://127.0.0.1:8081"

parser = argparse.ArgumentParser(description="Uploads file to img processing.")
parser.add_argument("path_image", metavar="path_image", type=str, help="path to file")

args = parser.parse_args()

with open(parser.parse_args().path_image, "rb") as f:
    im_b64 = base64.b64encode(f.read()).decode("utf8")

headers = {"Content-type": "application/json", "Accept": "text/plain"}
payload = json.dumps({"image": im_b64})
response = requests.post(f"{URL}/image", data=payload)
try:
    IMAGE_ID = response.json()["image_sha"]
except requests.exceptions.RequestException:
    print(response.text)
