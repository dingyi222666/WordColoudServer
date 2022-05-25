import json
import logging
from create_word_cloud import render, posseg_lcut
from aiohttp import web, web_request


async def generate_word_cloud(request_: web_request.Request):
    segment_text = await request_.text()
    segment_json = json.loads(segment_text)
    segment_json = segment_json['segment']
    logging.getLogger().info(f"segment_json: {segment_json}")
    segments = json.loads(segment_json)
    base64str = render(segments)
    logging.getLogger().info(f"base64str: {base64str}")
    return web.json_response(data={'result': base64str})


async def jieba_cut_2(request_: web_request.Request):
    segment_text = await request_.text()
    segment_json = json.loads(segment_text)
    segment = segment_json['segment']
    logging.getLogger().info(f"segment: {segment_json}")
    words = posseg_lcut(segment)
    logging.getLogger().info(f"words: {words}")
    return web.json_response(data={'result': words})


app = web.Application()
logging.basicConfig(level=logging.INFO)
app.add_routes([web.post('/generate_word_cloud', generate_word_cloud),
                web.post('/posseg_lcut', jieba_cut_2)])

if __name__ == '__main__':
    web.run_app(app, port=8080)
