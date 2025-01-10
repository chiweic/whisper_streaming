import asyncio
from websockets.asyncio.client import connect
import json
import logging
from pydub import AudioSegment
from pydub.utils import make_chunks


logging.basicConfig(level=logging.INFO)

async def hello():
    header={'user':'me', 'secret':'demo'}
    async with connect("ws://localhost:8000/ws/2112") as websocket:
        await websocket.send(json.dumps(header), text=True)
        message = await websocket.recv()
        logging.info(message)
        # open the audio wave
        audio = AudioSegment.from_file('demo.wav')
        chunks = make_chunks(audio_segment=audio, chunk_length=5000) # 5 seconds chunks
        # simulate bytes...
        for i, chunk in enumerate(chunks):
            # bytes...
            raw_data = chunk.raw_data()
            # send none-block
            # await websocket.send()
        # await websocket.send("Hello world again!", text=True)
        # message = await websocket.recv()
        # print(message)
        # wait until server told us we are done...


if __name__ == "__main__":
    asyncio.run(hello())