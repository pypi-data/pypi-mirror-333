import httpx
import aiohttp
import json
import os
import typing
from ..network.connection import Connection
from typing import Union

chats = typing.Literal['private', 'group', 'channel', 'null']
sticker_types = typing.Literal['regular', 'mask', 'null']

sync_client = httpx.Client()
async_client = httpx.AsyncClient()

class Text(object):
    def __init__(self, text_message: str):
        self.tm = text_message

    @property
    def bold(self):
        return f"*{self.tm}*"
    
    @property
    def italic(self):
        return f"_{self.tm}_"
    
    def addLink(self, link: str):
        return f"[{self.tm}]({link})"
    
    def addInfo(self, details: str):
        return f"```[{self.tm}]{details}```"

class User(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}
        
        self.id: int = self.result.get("id", 0)
        self.is_bot: bool = self.result.get("is_bot", False)
        self.first_name: str = self.result.get("first_name", "null")
        self.last_name: str = self.result.get("last_name", "null")
        self.username: str = self.result.get("username", "null")
        self.language_code: str = self.result.get("language_code", "null")
    
    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class ChatPhoto(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.small_file_id: str = self.result.get("small_file_id", "null")
        self.small_file_unique_id: str = self.result.get("small_file_unique_id", "null")
        self.big_file_id: str = self.result.get("big_file_id", "null")
        self.big_file_unique_id: str = self.result.get("big_file_unique_id", "null")

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class PhotoSize(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get("file_id", "null")
        self.file_unique_id: str = self.result.get("file_unique_id", "null")
        self.width: int = self.result.get("width", 0)
        self.height: int = self.result.get("height", 0)
        self.file_size: int = self.result.get("file_size", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)

class Animation(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get("file_id", "null")
        self.file_unique_id: str = self.result.get("file_unique_id", "null")
        self.width: int = self.result.get("width", 0)
        self.height: int = self.result.get("height", 0)
        self.duration: int = self.result.get("duration", 0)
        self.thumbnail: PhotoSize = PhotoSize(self.result.get("thumbnail", {}))
        self.file_name: str = self.result.get("file_name", "null")
        self.mime_type: str = self.result.get("mime_type", "octet/stream")
        self.file_size: int = self.result.get("file_size", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Audio(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get("file_id", "null")
        self.file_unique_id: str = self.result.get("file_unique_id", "null")
        self.duration: int = self.result.get("duration", 0)
        self.title: str = self.result.get("title", "null")
        self.file_name: str = self.result.get("file_name", "null")
        self.mime_type: str = self.result.get("mime_type", "octet/stream")
        self.file_size: int = self.result.get("file_size", 0)
    
    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Document(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get("file_id", "null")
        self.file_unique_id: str = self.result.get("file_unique_id", "null")
        self.thumbnail: PhotoSize = PhotoSize(self.result.get("thumbnail", {}))
        self.file_name: str = self.result.get("file_name", "null")
        self.mime_type: str = self.result.get("mime_type", "octet/stream")
        self.file_size: int = self.result.get("file_size", 0)
    
    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Video(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get("file_id", "null")
        self.file_unique_id: str = self.result.get("file_unique_id", "null")
        self.width: int = self.result.get("width", 0)
        self.height: int = self.result.get("height", 0)
        self.duration: int = self.result.get("duration", 0)
        self.file_name: str = self.result.get("file_name", "null")
        self.mime_type: str = self.result.get("mime_type", "octet/stream")
        self.file_size: int = self.result.get("file_size", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Voice(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get("file_id", "null")
        self.file_unique_id: str = self.result.get("file_unique_id", "null")

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Contact(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.phone_number: str = self.result.get("phone_number", "null")
        self.first_name: str = self.result.get("first_name", "null")
        self.last_name: str = self.result.get("last_name", "null")
        self.user_id: int = self.result.get("user_id", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class ContactArray(object):
    def __init__(self, contacts: list[Contact]):
        self.contacts = contacts

    def forEach(self) -> Contact:
        for contact in self.contacts:
            if isinstance(contact, Contact): return contact
            else: return Contact(contact)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Location(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.longitude: float = self.result.get("longitude", 0)
        self.latitude: float = self.result.get("latitude", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class File(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.id: str = self.result.get('file_id', 'null')
        self.unique_id: str = self.result.get("file_unique_id", 'null')
        self.size: int = self.result.get("file_size", 0)
        self.path: str = self.result.get("file_path", "null")

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Sticker(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.file_id: str = self.result.get('file_id', 'null')
        self.file_unique_id: str = self.result.get("file_unique_id", 'null')
        self.file_size: int = self.result.get("file_size", 0)
        self.type: sticker_types = self.result.get("type", 'null')
        self.width: int = self.result.get("width", 0)
        self.height: int = self.result.get("height", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class StickerSet(object):
    def __init__(self, result: dict):
        self.result = result

        self.name: str = self.result.get("name", "")
        self.title: str = self.result.get("title", "")
        self.stickers: list[Sticker] = [Sticker(stick) for stick in self.result.get("stickers", [])]
        self.thumbnail: PhotoSize = PhotoSize(self.result.get("thumbnail", {}))

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)

class InlineKeyboardButton(object):
    def __init__(self, text: str, url: str = None, callback_data: str = None):
        self.text = text
        if not url == None and not callback_data == None:
            raise ValueError("Cannot use Both `url` and `callback_data`")
        
        if url == None and callback_data == None:
            raise ValueError("Cannot dont use Both `url` and `callback_data`, require one")

        self.type = "url" if not url == None else "callback_data"
        self.depends = url if not url == None else callback_data

    def __str__(self):
        return f"<InlineButton text={self.text} depends={self.depends} type={self.type}>"


class InlineKeyboardMarkup(object):
    def __init__(self):
        self.keybuttons: list[list[dict[str, str]]] = []

    def addKeyboard(self, *buttons: list[InlineKeyboardButton]):
        self.keybuttons.append([])
        for button in buttons:
            if not isinstance(button, InlineKeyboardButton):
                raise ValueError("Invalid Keyboard type")
            
            self.keybuttons[-1].append(
                {
                    "text": button.text,
                    button.type: button.depends
                }
            )

        return self.keybuttons

    def __str__(self):
        return json.dumps(self.keybuttons, ensure_ascii=False, indent=2)
    
class Keyboard(object):
    def __init__(self, text: str, request_contact: bool = False, request_location: bool = False):
        self.text = text
        if not request_contact == False and not request_location == False:
            raise ValueError("Cannot use Both `request_contact` and `request_location`")
        
        if request_contact == False and request_location == False:
            raise ValueError("Cannot dont use Both `request_contact` and `request_location`, require one")

        self.type = "request_contact" if not request_contact == False else "request_location"
        self.depends = request_contact if not request_contact == False else request_location

class KeyboardMarkup(object):
    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = True):
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.keybuttons: list[list[dict[str, str]]] = []

    def addButton(self, *buttons: list[Keyboard]):
        self.keybuttons.append([])
        for button in buttons:
            if not isinstance(button, Keyboard):
                raise ValueError("Invalid Keyboard type")
            
            self.keybuttons[-1].append(
                {
                    "text": button.text,
                    "resize_keyboard": self.resize_keyboard,
                    "one_time_keyboard": self.one_time_keyboard,
                    button.type: button.depends
                }
            )

        return self.keybuttons

    def __str__(self):
        return json.dumps(self.keybuttons, ensure_ascii=False, indent=2)

class ReplyKeyboardMarkup(KeyboardMarkup):
    def __init__(self):
        super().__init__()

class Chat(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.id: int = self.result.get("id", 0)
        self.type: chats = self.result.get("type", 'null')
        self.title: str = self.result.get("title", "null")
        self.username: str = self.result.get("username", "null")
        self.photo: ChatPhoto = ChatPhoto(self.result.get("photo", {}))
        self.first_name: str = self.result.get("first_name", "null")
        self.last_name: str = self.result.get("last_name", "null")
        self.invite_link: str = self.result.get("invite_link", "")

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class Invoice(object):
    def __init__(self, result: dict = {}):
        self.result = result if result is not None else {}

        self.chat_id: Union[int, str] = self.result.get("chat_id", "")
        self.title: str = self.result.get("title", "")
        self.description: str = self.result.get("description", "")
        self.payload: str = self.result.get("payload", "")
        self.provider_token: str = self.result.get("provider_token", "")
        self.photo_url: str = self.result.get("photo_url", "")
        self.reply_to_message_id: int = self.result.get("reply_to_message_id", 0)
        self.reply_markup: Union[InlineKeyboardButton, Keyboard] = self.result.get("reply_markup", InlineKeyboardButton("", ""))
        self.prices: list = self.result.get("prices", [])
    
    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)

class Message(object):
    def __init__(self, token: str, result: dict):
        self.token = token
        self.bot_url = "https://tapi.bale.ai/bot"+self.token
        self.connection = Connection(self.token)
        self.result = result if result is not None else {}
        self.result = self.result.get("message", {}) if 'message' in self.result else self.result.get("callback_query", {}) if 'callback_query' in self.result else {}
    
        self.message_id: int = self.result.get("message_id", 0)
        self.from_user: User = User(self.result.get("from", {}))
        self.date: int = self.result.get("date", 0)
        self.timestamp: int = self.date
        self.chat: Chat = Chat(self.result.get("chat", {}))
        self.forward_from: User = User(self.result.get("forward_from", {}))
        self.forward_from_chat: Chat = Chat(self.result.get("forward_from_chat", {}))
        self.forward_from_message_id: int = self.result.get("forward_from_message_id", 0)
        self.forward_date: int = self.result.get("forward_date", 0)
        self.forward_timestamp: int = self.forward_date
        self.edit_date: int = self.result.get("edit_date", 0) if "edit_date" in self.result else self.result.get("edite_date", 0) if "edite_date" in self.result else 0
        self.text: str = self.result.get("text", "")
        self.animation: Animation = Animation(self.result.get("animation", {}))
        self.audio: Audio = Audio(self.result.get("audio", {}))
        self.voice: Voice = Voice(self.result.get("voice", {}))
        self.document: Document = Document(self.result.get("document", {}))
        self.video: Video = Video(self.result.get("video", {}))
        self.photo: list[PhotoSize] = [PhotoSize(ph) for ph in self.result.get("photo", [])]
        self.sticker: Sticker = Sticker(self.result.get("sticker", {}))
        self.caption: str = self.result.get("caption", "")
        self.contact: Contact = Contact(self.result.get("contact", {}))
        self.location: Location = Location(self.result.get("location", {}))
        self.new_chat_members: list[User] = [User(user) for user in self.result.get("new_chat_members", {})]
        self.left_chat_member: User = User(self.result.get("left_chat_member", {}))
        self.invoice: Invoice = Invoice(self.result.get("invoice", {}))
        self.successful_payment: dict = self.result.get("successful_payment", {})
        self.reply_markup: InlineKeyboardButton = InlineKeyboardButton(self.result.get("reply_markup", {}), "")
        self.callback_query: CallbackQuery = CallbackQuery(self.token, self.result)
    
    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
    @property
    def from_reply_message(self):
        return Message(self.token, {"message": self.result.get("reply_to_message", {})})
    
    def reply(
        self,
        text: str,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ):
        
        if not reply_markup == None:
            if isinstance(reply_markup, InlineKeyboardMarkup):
                json_data = {
                    "text": text,
                    "chat_id": self.chat.id,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "inline_keyboard": reply_markup.keybuttons
                    }
                }
            
            else:
                json_data = {
                    "text": text,
                    "chat_id": self.chat.id,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "keyboard": reply_markup.keybuttons
                    }
                }
        else:
            json_data = {
                "text": text,
                "chat_id": self.chat.id,
                "reply_to_message_id": self.message_id
            }

        return sync_client.post(
            self.bot_url+"/sendMessage",
            json=json_data
        ).json()
    
    async def asyncReply(
        self,
        text: str,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ):
        
        if not reply_markup == None:
            if isinstance(reply_markup, InlineKeyboardMarkup):
                json_data = {
                    "text": text,
                    "chat_id": self.chat.id,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "inline_keyboard": reply_markup.keybuttons
                    }
                }
            
            else:
                json_data = {
                    "text": text,
                    "chat_id": self.chat.id,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "keyboard": reply_markup.keybuttons
                    }
                }
        else:
            json_data = {
                "text": text,
                "chat_id": self.chat.id,
                "reply_to_message_id": self.message_id
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.bot_url+"/sendMessage", json=json_data) as resp:
                return await resp.json()
    
    def replyPhoto(
        self,
        photo: str,
        text: str = ""
    ):
        
        return self.connection.uploadSomething(photo, "photo", self.chat.id, text, self.message_id)
    
    async def asyncReplyPhoto(
        self,
        photo: str,
        text: str = ""
    ):
        
        return await self.connection.uploadAsyncSomething(photo, "photo", self.chat.id, text, self.message_id)
    
    def replyAudio(
        self,
        audio: str,
        text: str = ""
    ):
        
        return self.connection.uploadSomething(audio, "audio", self.chat.id, text, self.message_id)
    
    async def asyncReplyAudio(
        self,
        audio: str,
        text: str = ""
    ):
        
        return await self.connection.uploadAsyncSomething(audio, "audio", self.chat.id, text, self.message_id)
    
    def replyVideo(
        self,
        video: str,
        text: str = ""
    ):
        
        return self.connection.uploadSomething(video, "video", self.chat.id, text, self.message_id)

    async def asyncReplyVideo(
        self,
        video: str,
        text: str = ""
    ):
        
        return await self.connection.uploadAsyncSomething(video, "video", self.chat.id, text, self.message_id)
    
    def replyDocument(
        self,
        document: str,
        text: str = ""
    ):
        
        return self.connection.uploadSomething(document, "document", self.chat.id, text, self.message_id)

    async def asyncReplyDocument(
        self,
        document: str,
        text: str = "",
        filename: str = None
    ):
        
        return await self.connection.uploadAsyncSomething(document, "document", self.chat.id, text, self.message_id, 'null', None)

    def replyAnimation(
        self,
        animation: str,
        text: str = ""
    ):
        
        return self.connection.uploadSomething(animation, "animation", self.chat.id, text, self.message_id)

    async def asyncReplyAnimation(
        self,
        animation: str,
        text: str = ""
    ):
        
        return await self.connection.uploadAsyncSomething(animation, "animation", self.chat.id, text, self.message_id)
    
    def replyVoice(
        self,
        voice: str,
        text: str = ""
    ):
        
        return self.connection.uploadSomething(voice, "voice", self.chat.id, text, self.message_id)

    async def asyncReplyVoice(
        self,
        voice: str,
        text: str = ""
    ):
        
        return await self.connection.uploadAsyncSomething(voice, "voice", self.chat.id, text, self.message_id)

    def replyLocation(
        self,
        longitude: float,
        latitude: float,
        horizontal_accuracy: float = None,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ):
        
        if not reply_markup == None:
            if isinstance(reply_markup, InlineKeyboardMarkup):
                json_data = {
                    "chat_id": self.chat.id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "horizontal_accuracy": horizontal_accuracy,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "inline_keyboard": reply_markup.keybuttons
                    }
                }
            
            else:
                json_data = {
                    "chat_id": self.chat.id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "horizontal_accuracy": horizontal_accuracy,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "keyboard": reply_markup.keybuttons
                    }
                }
        else:
            json_data = {
                "chat_id": self.chat.id,
                "latitude": latitude,
                "longitude": longitude,
                "horizontal_accuracy": horizontal_accuracy,
                "reply_to_message_id": self.message_id
            }

        return sync_client.post(
            self.bot_url+"/sendLocation",
            json=json_data
        ).json()

    async def asyncReplyLocation(
        self,
        longitude: float,
        latitude: float,
        horizontal_accuracy: float = None,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ):
        
        if not reply_markup == None:
            if isinstance(reply_markup, InlineKeyboardMarkup):
                json_data = {
                    "chat_id": self.chat.id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "horizontal_accuracy": horizontal_accuracy,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "inline_keyboard": reply_markup.keybuttons
                    }
                }
            
            else:
                json_data = {
                    "chat_id": self.chat.id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "horizontal_accuracy": horizontal_accuracy,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "keyboard": reply_markup.keybuttons
                    }
                }
        else:
            json_data = {
                "chat_id": self.chat.id,
                "latitude": latitude,
                "longitude": longitude,
                "horizontal_accuracy": horizontal_accuracy,
                "reply_to_message_id": self.message_id
            }

        async with aiohttp.ClientSession() as session:
                async with session.post(self.bot_url+"/sendLocation", json=json_data) as resp:
                    return await resp.json()
    
    def replyContact(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = None,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ):
        
        if not reply_markup == None:
            if isinstance(reply_markup, InlineKeyboardMarkup):
                json_data = {
                    "chat_id": self.chat.id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "inline_keyboard": reply_markup.keybuttons
                    }
                }
            
            else:
                json_data = {
                    "chat_id": self.chat.id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "keyboard": reply_markup.keybuttons
                    }
                }
        else:
            json_data = {
                "chat_id": self.chat.id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "reply_to_message_id": self.message_id
            }

        return sync_client.post(
            self.bot_url+"/sendContact",
            json=json_data
        ).json()
    
    async def asyncReplyContact(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = None,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ):
        
        if not reply_markup == None:
            if isinstance(reply_markup, InlineKeyboardMarkup):
                json_data = {
                    "chat_id": self.chat.id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "inline_keyboard": reply_markup.keybuttons
                    }
                }
            
            else:
                json_data = {
                    "chat_id": self.chat.id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "reply_to_message_id": self.message_id,
                    "reply_markup": {
                        "keyboard": reply_markup.keybuttons
                    }
                }
        else:
            json_data = {
                "chat_id": self.chat.id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "reply_to_message_id": self.message_id
            }

        async with aiohttp.ClientSession() as session:
                async with session.post(self.bot_url+"/sendContact", json=json_data) as resp:
                    return await resp.json()
    
class CallbackQuery(object):
    def __init__(self, token: str, result: dict = {}):
        self.token = token
        self.result = result
        self.clicked_from_chat: int = self.result.get("chat_instance", 0)
        self.id: str = self.result.get("id", 0)
        self.inline_id: str = self.result.get("inline_message_id", 0)
        self.from_user: User = User(self.result.get("from", {}))
        self.data: str = self.result.get("data", "")
    
    @property
    def clicked_message(self) -> Message:
        return Message(token=self.token, result={"message": self.result.get("message", {})})

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class ForwardMessage(object):
    def __init__(self, result: dict):
        self.result = result
        
        self.message_id: int = self.result.get("message_id", 0)
        self.from_user: User = User(self.result.get("from", {}))
        self.date: int = self.result.get("date", 0)
        self.chat: Chat = Chat(self.result.get("chat", {}))
        self.forward_date: int = self.result.get("forward_date", 0)

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)
    
class SendMessage(object):
    def __init__(self, result: dict):
        self.result = result.get("result", {})
        
        self.message_id: int = self.result.get("message_id", 0)
        self.from_user: User = User(self.result.get("from", {}))
        self.date: int = self.result.get("date", 0)
        self.chat: Chat = Chat(self.result.get("chat", {}))
        self.text: str = self.result.get("text", "")

    def __str__(self):
        return json.dumps(self.result, ensure_ascii=False, indent=2)