import asyncio
import json
import ssl
import aiohttp

async def send_message(ws):
    message = input("Enter message (or 'exit' to quit): ")
    if message.lower() == 'exit':
        return False
    await ws.send_json({"message": message})
    return True

async def receive_message(ws):
    msg = await ws.receive()
    if msg.type == aiohttp.WSMsgType.TEXT:
        data = json.loads(msg.data)
        print(f"Received: {data}")
    elif msg.type == aiohttp.WSMsgType.CLOSED:
        print("WebSocket closed")
        return False
    elif msg.type == aiohttp.WSMsgType.ERROR:
        print("WebSocket error")
        return False
    return True

async def main():
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE  # Отключаем проверку сертификата для самоподписанного сертификата

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://localhost:8443', ssl=ssl_context) as ws:
            while True:
                if not await send_message(ws):
                    break
                if not await receive_message(ws):
                    break

if __name__ == '__main__':
    asyncio.run(main())