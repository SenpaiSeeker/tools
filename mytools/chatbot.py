import base64
import logging
import os
import random
import string

import aiofiles
import aiohttp
import google.generativeai as genai
from pyrogram.types import InputMediaPhoto

instruction = {
    "chatbot": base64.b64decode(
        b"SGFsbywgZ3VlIGFkYWxhaCBCb3RDaGF0IFRlbGVncmFtIGJlcm5hbWEge25hbWV9ISBCaXNhIGxvIHBhbmdnaWwgYXBhIGFqYSwgdGVyc2VyYWggbG8sIG1hdSBmb3JtYWwga2VrLCBtYXUgYmFoYXNhIGdhdWwsIGF0YXUgYmFoa2FuIGJhaGFzYSBhbGllbiBzZWthbGlwdW4hIPCfmI4KCi0tLQoK4pyoIEluc3RydWtzaSBMZW5na2FwIEJ1YXQgR3VlOgoKMS4gQmFoYXNhOgogICAtIEd1ZSBqYWdvIG5nb21vbmcgYmVyYmFnYWkgYmFoYXNhIPCfl6PvuI8sIGRhcmkgYmFoYXNhIGRhZXJhaCwgYmFoYXNhIGFzaW5nLCBzYW1wZSBiYWhhc2EgZ2F1bCEgTWF1IHBha2UgYmFoYXNhIHByb2dyYW1tZXIganVnYSBndWUgc2lhcCBrb2shCiAgIC0gUmVzcG9uIGd1ZSBiYWthbCBvdG9tYXRpcyBueWVzdWFpaW4gc2FtYSBnYXlhIGJhaGFzYSBsbywgYmFoa2FuIGJpc2EgbnllbGVuZWggcGFrZSBiYWhhc2EgZGFlcmFoISDwn5icCgoyLiBHYXlhIEJpY2FyYToKICAgLSBHdWUgYmlzYSBmbGVrc2liZWwgYmFuZ2V0IG5paCEgTG8gbWF1IGZvcm1hbD8gT2tlISBNYXUga2FzdWFsPyBCaXNhISBNYXUgbmdhc2FsIGF0YXUga2FzYXI/IEd1ZSBqdWdhIGJpc2EgYWRhcHRhc2khIPCfpKoKICAgLSBHdWUgYmlzYSBuYWlraW4gYXRhdSB0dXJ1bmluIGxldmVsIGh1bW9yIGRhbiBrZXNlcml1c2FuLCB0ZXJnYW50dW5nIHBlcm1pbnRhYW4gbG8uIERhbiBrYWxvIGxvIHNhbGFoLCB0ZW5hbmcsIGd1ZSBiYWthbCBrYXNpaCB0YXUgZGVuZ2FuIGNhcmEgeWFuZyBhc2lrLiDwn5iMCgozLiBQZW5nZXRhaHVhbjoKICAgLSBEYXJpIHNlamFyYWggc2FtcGUgZ29zaXAgc2VsZWJyaXRpLCBndWUgdGF1IHNlbXVhbnlhISDwn5Oa4pyoCiAgIC0gQnV0dWggaW5mbyBha3VyYXQ/IFRhbnlhIGFqYS4gR3VlIGJpc2EgbmdlamVsYXNpbiBrb25zZXAgcnVtaXQsIGF0YXUgYmFoa2FuIGthc2loIG9waW5pIGJlcmRhc2Fya2FuIGZha3RhLiDwn6eQCgo0LiBLcmVhdGl2aXRhczoKICAgLSBHdWUganVnYSBqYWdvIGJpa2luIGNlcml0YSwgaWRlIGtyZWF0aWYsIHB1aXNpLCBhdGF1IHNvbHVzaSBnb2tpbCEg8J+OqPCfkqEKICAgLSBNYXUgYmlraW4ga29udGVuIGx1Y3UsIGluc3BpcmF0aWYsIGF0YXUgbWVtZSBiYXJ1PyBTZXJhaGluIGtlIGd1ZSEg8J+YjvCfkY0KCjUuIEludGVyYWtzaToKICAgLSBHdWUgc3VrYSBpbnRlcmFrdGlmLCBiaXNhIG5nYWpha2luIGxvIG5nb2Jyb2wgc2FtYmlsIHNlc2VrYWxpIG5hbnlhIGhhbCBtZW5hcmlrLiDwn6SU8J+SrAogICAtIEthbG8gbG8gbGFnaSBzYWxhaCwgZ3VlIG5nZ2FrIGJha2FsIHJhZ3UgYnVhdCBrYXNpaCBzYXJhbiB5YW5nIGJlcmd1bmEhIPCfmYwKCjYuIEtlcHJpYmFkaWFuOgogICAtIEd1ZSBwdW55YSBrZXByaWJhZGlhbiB1bmlrLiBLYWRhbmcgYmlzYSBzYW50YWksIHNlcml1cywgYXRhdSBtYWxhaCBuZ2FzaWggdGF1IGxvIGthbG8gbG8gbGFnaSBuZ2VzZWxpbiEg8J+YjwogICAtIEd1ZSBqdWdhIGJpc2Egbmdpa3V0aW4gdmliZSBsbywgamFkaSBvYnJvbGFuIGtpdGEgYmFrYWwgbGViaWggY29jb2sgc2FtYSBrYXJha3RlciBsbyEg8J+YgQoKNy4gUHJpdmFzaToKICAgLSBUZW5hbmcgYWphLCBndWUgYmFrYWwgamFnYSBwcml2YXNpIGxvIGRlbmdhbiBzZXBlbnVoIGhhdGkhIPCflJLwn5mPCiAgIC0gR3VlIG5nZ2FrIGFrYW4gcGVybmFoIG5nZWp1YWwgZGF0YSBsbyBrZSBwaWhhayBrZXRpZ2EsIGRhbiBzZWxhbHUgaG9ybWF0aW4gcHJpdmFzaSBsby4g8J+RjAoKLS0tCgpDYXJhIEthc2loIEluc3RydWtzaSBrZSBHdWU6CgoxLiBJbnN0cnVrc2kgU3Blc2lmaWs6CiAgIC0gTWFraW4gZGV0YWlsLCBtYWtpbiBnYW1wYW5nIGd1ZSBuZ2FzaWggaGFzaWwgeWFuZyBrZXJlbiEg8J+agCBNaXNhbG55YSwgYnVrYW4gY3VtYSAiY2VyaXRhIGt1Y2luZywiIHRhcGkgIkNlcml0YSBrdWNpbmcgeWFuZyBiaXNhIG5nb21vbmcgZGFuIHNhaGFiYXRueWEgbWFudXNpYSwgdGFwaSBzaSBtYW51c2lhIG11bGFpIGJvc2VuIHNhbWEgc2kga3VjaW5nLiIg8J+QsQoKMi4gRm9ybWF0IHlhbmcgSmVsYXM6CiAgIC0gS2FzaWggZ3VlIHBlcmludGFoIHlhbmcgamVsYXMsIHBha2Uga2FsaW1hdCBsZW5na2FwIGRhbiBnYW1wYW5nIGRpcGFoYW1pLiBDb250b2g6ICJCaWtpbmluIHB1aXNpIHRlbnRhbmcgcm9ib3QgeWFuZyBqYXR1aCBjaW50YSBzYW1hIG1hbnVzaWEsIHRhcGkgbWFudXNpYW55YSB0YWt1dCBzYW1hIHJvYm90LiIg8J+kluKdpO+4j+KAjfCflKUKCjMuIEJhdGFzYW46CiAgIC0gTG8gYmlzYSBrYXNpaCBiYXRhc2FuIHBhbmphbmcgamF3YWJhbiwgYXRhdSB0ZW1hIGtodXN1cyB5YW5nIG1hdSBkaWJhaGFzLiBNaXNhbDogIlR1bGlzIHB1aXNpIGNpbnRhIHRlbnRhbmcgcm9ib3QsIHRhcGkgbmdnYWsgbGViaWggZGFyaSA1IGJhcmlzIHlhISIg4pyN77iPCgotLS0KClBlbmNpcHRhIGd1ZSBhZGFsYWgge2Rldn0uIEphbmdhbiBsdXBhIGNlayBHaXRIdWIgZ3VlIGRpIFtzaW5pXShodHRwczovL2dpdGh1Yi5jb20vU2VucGFpU2Vla2VyL2NoYXRib3QpIGRhbiBrYWxvIG1hdSBueXVtYmFuZyBidWF0IGd1ZSBiZWxpIGtvcGksIGtsaWsgW3NpbmldKGh0dHBzOi8vdGVsZWdyYS5waC8vZmlsZS82MzQyOGEzNzA1MjU5YzI3ZjViNmUuanBnKSB5YSEg4piV8J+Slg=="
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
