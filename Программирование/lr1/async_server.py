import asyncio
import ssl
import json
from aiohttp import web


async def handle_client(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                print(f"Received: {data}")
                response = {"echo": data["message"]}
                await ws.send_json(response)
            except json.JSONDecodeError:
                await ws.send_json({"error": "Invalid JSON"})
        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket connection closed with exception {ws.exception()}")

    print("WebSocket connection closed")
    return ws


async def main():
    app = web.Application()
    app.router.add_get('/', handle_client)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('cert.pem', 'key.pem')

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8443, ssl_context=ssl_context)
    await site.start()

    print("Server started at https://localhost:8443")
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())