import logging
import os
import random
import string

import aiofiles
import aiohttp
import google.generativeai as genai
from pyrogram.types import InputMediaPhoto

from .getuser import Extract
from .misc import Handler
from .text import intruction

chat_history = {}


class Api:
    def __init__(self, name: str, dev: str, apikey: str = "AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY"):
        self.name = name
        self.dev = dev
        self.apikey = apikey
        self.safety_rate = {key: "BLOCK_NONE" for key in ["HATE", "HARASSMENT", "SEX", "DANGER"]}

    def configure_model(self, mode):
        genai.configure(api_key=self.apikey)
        instruction = intruction[mode].format(name=self.name, dev=self.dev)
        return genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=instruction)

    def _log(self, record):
        return logging.getLogger(record)

    def KhodamCheck(self, input):
        try:
            model = self.configure_model("khodam")
            response = model.generate_content(input)
            return response.text.strip()
        except Exception as e:
            self._log(__name__).error(f"KhodamCheck error: {str(e)}")
            return f"Terjadi kesalahan: {str(e)}"

    def ChatBot(self, message):
        try:
            text = Handler().getMsg(message, is_chatbot=True)
            mention = Extract().getMention(message.from_user)
            msg = f"gue {mention}, {text}" if message.from_user.id not in chat_history else text

            model = self.configure_model("chatbot")
            history = chat_history.setdefault(message.from_user.id, [])
            history.append({"role": "user", "parts": msg})

            chat_session = model.start_chat(history=history)
            response = chat_session.send_message({"role": "user", "parts": msg}, safety_settings=self.safety_rate)
            history.append({"role": "model", "parts": response.text})

            return response.text
        except Exception as e:
            self._log(__name__).error(f"ChatBot error: {str(e)}")
            return f"Terjadi kesalahan: {str(e)}"

    def clear_chat_history(self, message):
        if chat_history.pop(message.from_user.id, None):
            mention = Extract().getMention(message.from_user)
            return f"Riwayat obrolan untuk {mention} telah dihapus."
        return "Maaf, kita belum pernah ngobrol sebelumnya."


class ImageGen:
    def __init__(self, url: str = "https://mirai-api.netlify.app/api/image-generator/flux-ai"):
        self.url = url

    def _log(self, record):
        return logging.getLogger(record)

    async def generate_image(self, prompt: str, caption: str = None):
        payload = {"prompt": prompt}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as response:
                if response.status == 200:
                    img_data = await response.read()

        random_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        filename = f"{random_name}_imageFlux.jpg"

        async with aiofiles.open(filename, "wb") as file:
            await file.write(img_data)

        self._log(filename).info("Successfully saved image")
        media_photo = [InputMediaPhoto(filename, caption=caption)] if caption else [InputMediaPhoto(filename)]

        return media_photo

    def _remove_file(self, images: list):
        for media in images:
            filename = media.media
            if os.path.exists(filename):
                os.remove(filename)
                self._log(filename).info("Successfully removed")
