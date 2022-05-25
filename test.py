import asyncio
import base64
import io
import json

import aiohttp
import matplotlib.pyplot as plt
from PIL import Image
from create_word_cloud import render
from aiohttp import request


# convert base64 to PIL image
def base64_to_pil(base64_str):
    imgdata = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(imgdata))


async def fetch(session, url, data):
    async with session.post(url, data=json.dumps(data)) as response:
        return await response.text()


# read file from local,use async
async def read_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        return f.read()


async def main():
    async with aiohttp.ClientSession() as session:
        # json_base64 = await fetch(session, "http://localhost:8080/generate_word_cloud", {
        #     "segment": await read_file("data/data.json")
        # })
        # print(json_base64)
        # base64str = json.loads(json_base64)['result']
        # print(base64str)
        # img = base64_to_pil(base64str)
        # show_pil_image(img)
        words = await fetch(session, "http://localhost:8080/posseg_lcut", {
            "segment": "摸摸"
        })
        print(words)
        print(json.loads(words))
        await session.close()


# show PIL image with matplotlib
def show_pil_image(img):
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    asyncio.run(main())
