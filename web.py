import os
from aiohttp import web

async def home(request):
    return web.Response(text="OK")

async def start_web():
    app = web.Application()
    app.router.add_route("*", "/", home)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ["PORT"])  # 🔑 required on Koyeb
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 Web server running on port {port}")
