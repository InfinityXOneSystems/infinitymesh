import asyncio
from nats.aio.client import Client as NATS

async def main():
    nc = NATS()
    await nc.connect("nats://127.0.0.1:4222")
    await nc.publish("mesh.prompt", b"Mesh Activation Test")
    await nc.flush()
    await nc.close()

asyncio.run(main())
