import httpx
import random
import requests
import aiohttp
import os
import json
import typing

thing_types = typing.Literal[
    'document', 'photo',
    'voice', 'video',
    'animation', 'audio'
]

class Connection(object):
    def __init__(
        self,
        token: str
    ): 
        self.token = token
        self.url = "https://tapi.bale.ai/bot"+self.token
        self.file_url = f"https://tapi.bale.ai/file/bot{self.token}/"
        self._sync = httpx.Client()
        self._async = httpx.AsyncClient()

    def createConnection(
        self,
        method: str,
        input: dict = {}
    ):
        return self._sync.post(
            self.url+"/"+method,
            json=input
        ).json()
    
    async def createAsyncConnection(
        self,
        method: str,
        input: dict = {}
    ):

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url+"/"+method, json=input) as resp:
                e = await resp.json()
                return e 
            
    def makeFilename(self):
        return f"Balegram_{random.randint(1000, 99999999999)}"
    
    def uploadSomething(
        self,
        thing: str,
        thing_type: thing_types,
        chat_id: int,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup = None
    ):
        
        if thing.startswith("http"):
            return requests.post(
                self.url+f"/send{thing_type.title()}",
                params={
                    "chat_id": chat_id,
                    "caption": caption,
                    "reply_to_message_id": reply_to_message_id,
                    thing_type: thing,
                    "reply_markup": None if reply_markup is None else reply_markup.keybuttons
                }
            ).json()
        
        elif os.path.exists(thing) and os.path.isfile(thing):
            return requests.post(
                self.url+f"/send{thing_type.title()}",
                params={
                    "chat_id": chat_id,
                    "caption": caption,
                    "reply_to_message_id": reply_to_message_id,
                    "reply_markup": None if reply_markup is None else reply_markup.keybuttons
                },
                files={
                    thing_type: open(thing, 'rb').read()
                }
            ).json()
        
        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            str(thing_type).title()
        ))

    async def uploadAsyncSomething(
        self,
        thing: str,
        thing_type: thing_types,
        chat_id: int,
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup = None,
        filename: str = None
    ):

        if thing.startswith("http"):
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url+f"/send{thing_type.title()}", json={
                    "chat_id": chat_id,
                    "caption": caption,
                    "reply_to_message_id": reply_to_message_id,
                    thing_type: thing,
                    "reply_markup": None if reply_markup is None else reply_markup.keybuttons
                }) as resp:
                    return await resp.json()
        
        elif os.path.exists(thing) and os.path.isfile(thing):
            async with aiohttp.ClientSession() as session:
                form_data = aiohttp.FormData()
                form_data.add_field("chat_id", str(chat_id))
                form_data.add_field("caption", caption)
                form_data.add_field("reply_to_message_id", str(reply_to_message_id) if not reply_to_message_id is None else '')
                form_data.add_field("reply_markup", 'null' if reply_markup is None else json.dumps(reply_markup.keybuttons, ensure_ascii=False))
                with open(thing, 'rb') as file:
                    file_content = file.read()
                    form_data.add_field(thing_type, file_content, filename=filename if not filename is None else self.makeFilename())
                async with session.post(self.url+f"/send{thing_type.title()}", data=form_data) as resp:
                    return await resp.json()
        
        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            str(thing_type).title()
        ))
