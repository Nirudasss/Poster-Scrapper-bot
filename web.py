import os
from aiohttp import web

async def home(request):
    return web.Response(text="OK")

app = web.Application()

# Accept GET, HEAD, OPTIONS – Koyeb health checks
app.router.add_route("*", "/", home)

if __name__ == "__main__":
    web.run_app(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
