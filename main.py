import mimetypes
import os
import uuid

from aiohttp import web
from dotenv import load_dotenv

import magic 

load_dotenv()

PORT = int(os.getenv("PORT", ""))
STATIC_DIR = os.getenv("STATIC_DIR")
STATIC_HOST = os.getenv("STATIC_HOST", "")
STATIC_PATH = os.getenv("STATIC_PATH", "")

os.makedirs(STATIC_DIR, exist_ok=True)


async def handle_post(request: web.Request) -> web.Response:
    if request.body_exists:
        body = await request.read()
        mime = magic.from_buffer(body, mime=True)
        ext = mimetypes.guess_extension(mime, strict=True) or ""
        filename = f"{uuid.uuid4()}{ext}"
        with open(f"{STATIC_DIR}/{filename}", 'wb') as out:
            out.write(body)
            return web.json_response({"url": f"{STATIC_HOST}/{filename}"})
    return web.HTTPInternalServerError(reason="Something went wrong")


async def handle_get(request: web.Request) -> web.Response:
    filename = request.match_info["filename"]
    try:
        with open(f"{STATIC_DIR}/{filename}", 'rb') as f:
            content = f.read()
        os.remove(f"{STATIC_DIR}/{filename}")
        return web.Response(body=content, status=200, content_type=mimetypes.guess_type(filename)[0])
    except FileNotFoundError:
        return web.HTTPNotFound()


def main():
    app = web.Application()
    app.router.add_post("/", handle_post)
    app.router.add_get("/{filename}", handle_get)
    web.run_app(app, port=PORT)


if __name__ == '__main__':
    main()
