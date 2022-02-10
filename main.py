import json
import asyncio
import websockets
import requests

url="wss://cluster.vtbs.moe"

class DDhttp_buff:
    def __init__(self,json_str):
        json_obj=json.loads(json_str)
        self.key=json_obj['key']
        self.type=json_obj['data']['type']
        self.url=json_obj['data']['url']
        print([self.key,self.type,self.url])

    def conct_live(self):
        if self.type == 'http':
            return requests.get(self.url).content

async def get_data(websocket):
    while True:
        await websocket.send("DDhttp")
        response_str=await websocket.recv()
        print(response_str)
        dd_obj=DDhttp_buff(response_str)
        #print({"key":dd_obj.key,"data":str(dd_obj.conct_live())})
        await websocket.send(json.dumps(str({"key":dd_obj.key,"data":dd_obj.conct_live()})))
        print("done")

async def main_logic():
    async with websockets.connect(url) as websocket:
        await get_data(websocket)

asyncio.get_event_loop().run_until_complete(main_logic())
