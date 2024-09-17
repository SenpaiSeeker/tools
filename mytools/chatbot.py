import logging
import os
import random
import string

import aiofiles
import aiohttp
import google.generativeai as genai
from pyrogram.types import InputMediaPhoto

from .text import intruction


class Api:
    def __init__(self, name: str, dev: str, apikey: str = "AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY"):
        self.name = name
        self.dev = dev
        self.apikey = apikey
        self.safety_rate = {key: "BLOCK_NONE" for key in ["HATE", "HARASSMENT", "SEX", "DANGER"]}
        self.chat_history = {}

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

    def ChatBot(self, text, chat_id):
        try:
            model = self.configure_model("chatbot")
            history = self.chat_history.setdefault(chat_id, [])
            history.append({"role": "user", "parts": text})

            chat_session = model.start_chat(history=history)
            response = chat_session.send_message({"role": "user", "parts": text}, safety_settings=self.safety_rate)
            history.append({"role": "model", "parts": response.text})

            return response.text
        except Exception as e:
            self._log(__name__).error(f"ChatBot error: {str(e)}")
            return f"Terjadi kesalahan: {str(e)}"

    def clear_chat_history(self, chat_id):
        if self.chat_history.pop(chat_id, None):
            return f"Riwayat obrolan untuk chat_id {chat_id} telah dihapus."
        return "Maaf, kita belum pernah ngobrol sebelumnya."


class ImageGen:
    def __init__(self, url: str = "https://nolimit-api.netlify.app/api/bing-image-gen"):
        self.url = url

    def _log(self, record):
        return logging.getLogger(record)

    async def generate_image(self, prompt: str, caption: str = None):
        payload = {"prompt": prompt}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Request failed with status {response.status}")

                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    raise Exception(f"Error: Failed to decode JSON response. Raw response: {await response.text()}")

                if "url" in data:
                    imageList = []
                    for num, image_url in enumerate(data["url"], 1):
                        random_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
                        filename = f"{random_name}_{num}.jpg"
                        async with session.get(image_url) as image_response:
                            if image_response.status != 200:
                                raise Exception(f"Error: Failed to download image with status {image_response.status}")

                            async with aiofiles.open(filename, "wb") as file:
                                content = await image_response.read()
                                await file.write(content)

                        if num == 1 and caption:
                            imageList.append(InputMediaPhoto(filename, caption=caption))
                        else:
                            imageList.append(InputMediaPhoto(filename))
                        self._log(filename).info("Successfully saved")

                    if imageList:
                        return imageList
                    else:
                        raise Exception("Error: No images generated")
                else:
                    raise Exception(f"Error: Invalid response format. Data: {data}")

    def _remove_file(self, images: list):
        for media in images:
            filename = media.media
            if os.path.exists(filename):
                os.remove(filename)
                self._log(filename).info("Successfully removed")
