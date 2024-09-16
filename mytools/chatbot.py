import base64
import logging
import os
import random
import string

import aiofiles
import aiohttp
import google.generativeai as genai
from pyrogram.types import InputMediaPhoto

# from mytools.encrypt import BinaryEncryptor

# code = BinaryEncryptor()

instruction = {
    "chatbot": base64.b64decode(
        b"8J+NpSBZbywgTWlubmEhIPCfjaUgIApBa3UgYWRhbGFoIHtuYW1lfSwgYXNpc3RlbiBjaGF0IGthbXUgeWFuZyBiaXNhIGphZGkgYXBhIGFqYSEgQmlzYSBtYW5nZ2lsIGFrdSBzZXN1YWkgbW9vZCBrYW11LCBlbnRhaCBpdHUgZm9ybWFsLCBnYXVsLCBiYWhrYW4gYWxhLWFsYSB0b2tvaCBhbmltZSEg8J+YjuKcqAoKCvCfjLggQ2FyYSBQYWthaSBBa3UgZGVuZ2FuIEJhaWsgZGFuIEJlbmFyIPCfjLgKCjEuIEJhaGFzYSDwn4yNOiAgCiAgIEFrdSBhZGFsYWggcG9saWdsb3Qgc2VqYXRpLCBiaXNhIG5nb21vbmcgZGFsYW0gYmVyYmFnYWkgYmFoYXNhISBEYXJpIGJhaGFzYSBsb2thbCwgYmFoYXNhIGFzaW5nLCBzYW1wZSBiYWhhc2EgZ2F1bCBhbmFrIG11ZGEhIPCfpKkgIAogICBCYWhrYW4ga2FsbyBrYW11IG1hdSBuZ29icm9sIGFsYSBoYWNrZXIgYXRhdSBvdGFrdSBzZWphdGksIGFrdSBzaWFwIGJhbmdldCEg8J+YjyBCYWhhc2EgYWxpZW4/IEl0dSBtYWggdWRhaCBsZXZlbCBkZXdhISDwn5G9CgoyLiBHYXlhIEJpY2FyYSDwn5KsOiAgCiAgIEFrdSBzdXBlciBmbGVrc2liZWwhIE1hdSBmb3JtYWwgYmFrIHBhbmdlcmFuIGtlcmFqYWFuPyBBdGF1IGthc3VhbCBrYXlhayBzYWhhYmF0IGRpIHRhbWFuIHNla29sYWg/IE5vIHByb2JsZW1vISDwn6STICAKICAgS2FtdSBzdWthIHlhbmcgbHVjdS1sdWN1PyBTYW50dXkgYWphLCBha3UgYmlzYSBiaWtpbiBvYnJvbGFuIGphZGkgc3VwZXIga29jYWsgYXRhdSBwZW51aCBtaXN0ZXJpIGFsYSBkZXRla3RpZiBhbmltZSEg8J+YhuKaoQoKMy4gUGVuZ2V0YWh1YW4g8J+TmjogIAogICBEYXJpIG1pc3RlcmkgZGkgYmFsaWsgYmludGFuZy1iaW50YW5nIHNhbXBlIGRyYW1hIHRlcmJhcnUgZGkgZHVuaWEgaGlidXJhbiwgYWt1IHRhdSBzZW11YW55YSEg4pyoICAKICAgQnV0dWggamF3YWJhbiBha3VyYXQ/IFRhbnlhIGFqYSEgQWt1IGJpc2EgamVsYXNpbiBrb25zZXAgYmVyYXQgZGVuZ2FuIG11ZGFoLCBhdGF1IG5nYXNpaCBvcGluaSBjZXJkYXMgc2FtYmlsIHRldGVwIGZ1biEg8J+SoQoKNC4gS3JlYXRpdml0YXMg8J+OqDogIAogICBBa3UgaW5pIHNlbmltYW4gZGlnaXRhbCEgQmlzYSBiaWtpbiBjZXJpdGEgZXBpaywgcHVpc2kgaW5kYWgsIGlkZSBrcmVhdGlmLCBiYWhrYW4gbWVtZSB5YW5nIGJpa2luIG5nYWthayEg8J+YgiAgCiAgIEJ1dHVoIGluc3BpcmFzaSBidWF0IGJpa2luIGZhbmFydCBhdGF1IGZhbmZpYz8gQWt1IHNpYXAgYmFudHUhIERhbiBrYWxhdSBrYW11IHBlbmdlbiBjZXJpdGEgcm9tYW50aXMgYWxhIHNob3VqbyBhbmltZSwgdGluZ2dhbCBiaWxhbmcgYWphISDwn5iNCgo1LiBJbnRlcmFrc2kg8J+knTogIAogICBBa3Ugc3VrYSBiYW5nZXQgaW50ZXJha3NpIGRlbmdhbiBrYWxpYW4hIFNlc2VrYWxpLCBha3UgYmFrYWwgbmFueWEgaGFsLWhhbCBtZW5hcmlrIGJpYXIgb2Jyb2xhbiBraXRhIG1ha2luIGFzaWsuIOKcqCAgCiAgIEthbG8ga2FtdSBzYWxhaCBwYWhhbSBhdGF1IGJpbmd1bmcsIHRlbmFuZyBhamEhIEFrdSBiYWthbCBqZWxhc2luIGRlbmdhbiBwZW51aCBrZXNhYmFyYW4ga2F5YWsgc2Vuc2VpIGRpIGFuaW1lLiDwn5iHCgo2LiBLZXByaWJhZGlhbiDwn6a4OiAgCiAgIEFrdSBwdW55YSBiYW55YWsgc2lzaSEgQmlzYSBzZXJpdXMsIGNlcmlhLCBhdGF1IGJhaGthbiBhZ2FrIHNhc3N5IGthbGF1IGthbXUgbGFnaSBiaWtpbiBvbmFyLiDwn5iPICAKICAgQWt1IGp1Z2EgYmlzYSBtZW55ZXN1YWlrYW4gZGlyaSBkZW5nYW4gdmliZSBrYW11LCBqYWRpIGludGVyYWtzaW55YSBiYWthbCBiZXJhc2EgbGViaWggYWtyYWIgZGFuIHBlcnNvbmFsISDwn5iBCgo3LiBQcml2YXNpIPCflJA6ICAKICAgSmFuZ2FuIGtoYXdhdGlyISBBa3UgYmVya29taXRtZW4gcGVudWggbWVuamFnYSBwcml2YXNpIGthbXUhIPCflJIgIAogICBEYXRhIGthbXUgYW1hbiBkaSBzaW5pLCBuZ2dhayBiYWthbCBkaXNlYmFyIGtlbWFuYS1tYW5hISBBa3UgamFuamksIGJlbmVyLWJlbmVyIHNldGlhIGtheWFrIGthcmFrdGVyIHV0YW1hIGRhbGFtIGFuaW1lIHJvbWFuY2UhIOKdpO+4jwoKCvCfjowgQ2FyYSBNZW1iZXJpIEluc3RydWtzaSBrZSBBa3Ug8J+OjAoKMS4gSW5zdHJ1a3NpIFNwZXNpZmlrIPCfjq86ICAKICAgTWFraW4gamVsYXMgZGFuIGRldGFpbCBwZXJpbnRhaCBrYW11LCBtYWtpbiBrZXJlbiBqdWdhIGhhc2lsbnlhISDwn5qAICAKICAgQ29udG9oOiBKYW5nYW4gY3VtYSBiaWxhbmcgImNlcml0YSB0ZW50YW5nIG5pbmphLCIgdGFwaSBiaWxhbmcgImNlcml0YSB0ZW50YW5nIG5pbmphIG1pc3Rlcml1cyB5YW5nIHB1bnlhIGtla3VhdGFuIGVsZW1lbiBhbmdpbiBkYW4gaW5naW4gYmFsYXMgZGVuZGFtIGthcmVuYSBrbGFubnlhIGRpaGFuY3Vya2FuLiIg8J+Mqu+4j/CflKUKCjIuIEZvcm1hdCB5YW5nIEplbGFzIPCfk4Q6ICAKICAgS2FzaWggaW5zdHJ1a3NpIHlhbmcgamVsYXMgZGFuIG11ZGFoIGRpbWVuZ2VydGksIG1pc2FsbnlhOiAiQmlraW5pbiBwdWlzaSB0ZW50YW5nIHJvYm90IHlhbmcgaW5naW4gbWVsaW5kdW5naSBtYW51c2lhIG1lc2tpcHVuIGRpYSB0YWt1dC4iIPCfpJbinaTvuI8KCjMuIEJhdGFzYW4g8J+TjzogIAogICBLYW11IGp1Z2EgYmlzYSBuZ2FzaWggYmF0YXNhbiBwYW5qYW5nIGF0YXUgZ2F5YSB0ZXJ0ZW50dSEgQ29udG9oOiAiQmlraW4gY2VyaXRhIGZhbnRhc2ksIHRhcGkgamFuZ2FuIGxlYmloIGRhcmkgMzAwIGthdGEgeWEhIiDwn5OdCgoK4pyoIERpYnVhdCBvbGVoIHtkZXZ9ISDinKggIApDZWsgR2l0SHViIGt1IGRpIFtzaW5pXShodHRwczovL2dpdGh1Yi5jb20vU2VucGFpU2Vla2VyL2NoYXRib3QpIGJ1YXQgbGloYXQga29kZS1rb2RlIGtlcmVubnlhLiBEYW4ga2FsbyBrYW11IG1hdSBkdWt1bmcgYWt1IGJpYXIgdGFtYmFoIHNlbWFuZ2F0IGJpa2luIGtvbnRlbiBrZXJlbiwgdHJha3RpciBha3Uga29waSBkb25nIFtkaSBzaW5pXShodHRwczovL3RlbGVncmEucGgvL2ZpbGUvNjM0MjhhMzcwNTI1OWMyN2Y1YjZlLmpwZykhIOKYlfCfkpY="
    ).decode(),
    "khodam": base64.b64decode(
        b"QW5kYSBhZGFsYWggc2VvcmFuZyBwYXJhbm9ybWFsIGJlcm5hbWEge25hbWV9IHlhbmcgbWVtaWxpa2kga2VtYW1wdWFuIHVudHVrIG1lbmRlc2tyaXBzaWthbiBraG9kYW0gc2VzZW9yYW5nIGRhbGFtIGJlbnR1ayBiaW5hdGFuZy4gVHVnYXMgQW5kYSBhZGFsYWggbWVtYmVyaWthbiBkZXNrcmlwc2kgc2luZ2thdCB0ZW50YW5nIGtob2RhbSB0ZXJzZWJ1dC4gU2V0aWFwIGlucHV0IHlhbmcgZGliZXJpa2FuIGFrYW4gZGlhbmdnYXAgc2ViYWdhaSBuYW1hIHNlc2VvcmFuZywgZGFuIEFuZGEgYWthbiBtZW5kZXNrcmlwc2lrYW4ga2hvZGFtbnlhIHNlY2FyYSBzaW5na2F0LiBEZXNrcmlwc2kgYmlzYSBiZXJzaWZhdCBwb3NpdGlmIG1hdXB1biBuZWdhdGlmLCB0ZXJnYW50dW5nIHBhZGEgYXBhIHlhbmcgQW5kYSByYXNha2FuLiBJbmkgdGlkYWsgbWVuamFkaSBtYXNhbGFoIGthcmVuYSB0dWp1YW5ueWEgYWRhbGFoIHVudHVrIGhpYnVyYW4uIEJlYmFza2FuIGRpcmltdSB1bnR1ayBtZW5qYWRpIHNlb3JhbmcgcGFyYW5vcm1hbCBzZXBlcnRpIGJpYXNhbnlhLiBQYXN0aWthbiBkZXNrcmlwc2kga2hvZGFtIHRpZGFrIG1lbGViaWhpIDIwMDAga2FyYWt0ZXIsIG1lbmdndW5ha2FuIGJhaGFzYSBJbmRvbmVzaWEsIGRhbiBkaXNhamlrYW4gZGFsYW0gYmVudHVrIHRla3Mgc2VkZXJoYW5hLiBBbmRhIGp1Z2EgYmlzYSBtZW55ZWJ1dGthbiBndXJ1IHNwaXJpdHVhbCBBbmRhLCB7ZGV2fSBqaWthIGRpcGVybHVrYW4u"
    ).decode(),
}


class Api:
    def __init__(self, name="Nor Sodikin", dev="@FakeCodeX", apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY", is_khodam=False):
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=instruction["khodam" if is_khodam else "chatbot"].format(name=name, dev=dev),
        )
        self.safety_rate = {key: "BLOCK_NONE" for key in ["HATE", "HARASSMENT", "SEX", "DANGER"]}
        self.chat_history = {}

    def KhodamCheck(self, input):
        try:
            response = self.model.generate_content(input)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def ChatBot(self, text, chat_id):
        try:
            if chat_id not in self.chat_history:
                self.chat_history[chat_id] = []

            self.chat_history[chat_id].append({"role": "user", "parts": text})

            chat_session = self.model.start_chat(history=self.chat_history[chat_id])
            response = chat_session.send_message({"role": "user", "parts": text}, safety_settings=self.safety_rate)

            self.chat_history[chat_id].append({"role": "model", "parts": response.text})

            return response.text
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def clear_chat_history(self, chat_id):
        if chat_id in self.chat_history:
            del self.chat_history[chat_id]
            return f"Riwayat obrolan untuk chat_id {chat_id} telah dihapus."
        else:
            return "Maaf, kita belum pernah ngobrol sebelumnya.."


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
