import asyncio
import aiohttp
import sqlite3
import datetime
from nats.aio.client import Client as NATS

OLLAMA = "http://host.docker.internal:11434/api/generate"
DB_PATH = r"C:\InfinityMesh\memory\state\memory.db"

async def handle_message(msg):
    prompt = msg.data.decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            OLLAMA,
            json={"model":"llama3","prompt":prompt,"stream":False}
        ) as r:
            response_text = await r.text()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO audit VALUES (?, ?, ?)",
              ("mesh_event", "nats_route", datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

    print("EVENT_PROCESSED")

async def main():
    nc = NATS()
    await nc.connect("nats://127.0.0.1:4222")
    await nc.subscribe("mesh.prompt", cb=handle_message)
    print("MESH_SUBSCRIBED")

    # Run forever
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
