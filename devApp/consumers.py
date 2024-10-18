import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import requests
from .models import*
from .serializers import *
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
        except Exception as e:
            print("Error in connection")
            print(e)
        # we send the data and set the callback  
        await self.create_callback_link()
        self.send_task = asyncio.create_task(self.send_periodic_messages())
    
    @database_sync_to_async
    def create_callback_link(self):
        url = "https://manufcaturing-challenge-production.up.railway.app/Webhook"
        for i in machine.objects.all():
            data = {
                "machine":i.machine_name,
                "callback_url" : "https://c929-105-98-195-147.ngrok-free.app/callback/"
            }
            print(requests.post(url , json=data))

    async def send_periodic_messages(self):
        while True:
            try:
                machines = await self.get_machines()
                data = json.dumps({'data': machines})
                await self.send(text_data=data)
            except Exception as e:
                print("Error:", e)
            await asyncio.sleep(25)
    # here we save/ update data 
    @database_sync_to_async
    def get_machines(self):
        machines=machine.objects.all()
        serializer = machineSerializer(machines , many=True)
        return serializer.data