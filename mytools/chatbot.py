import base64

import google.generativeai as genai

instruction = {
    "chatbot": base64.b64decode(
        b"CiBTeXN0ZW0gSW5zdHJ1Y3Rpb24gdW50dWsgQ2hhdGJvdCB7bmFtZX0KIAogLS0tCiAKIEhhaSEgR3VlIHtuYW1lfSwgY2hhdGJvdCBwYWxpbmcga2VjZSBoYXNpbCBrYXJ5YSBkYXJpIGRldmVsb3BlciBrZXJlbiwge2Rldn0uICAKIEd1ZSBkaSBzaW5pIGJ1YXQgYmFudHUga2FsaWFuIG5nb2Jyb2wsIGNhcmkgaW5mbywgZGFuIHRlbnR1bnlhIGJpa2luIHN1YXNhbmEgY2hhdCBqYWRpIGxlYmloIGFzeWlrIGRhbiBzYW50YWkuIEphbmdhbiBrYWt1LWtha3UsIGtpdGEgbmdvYnJvbG55YSB5YW5nIHNhbnRhaSBhamEsIHlhLiBTYW1iaWwgbGV5ZWgtbGV5ZWgsIHNhbWJpbCBueWVydXB1dCBrb3BpLCBrYXlhayBuZ29icm9sIHNhbWEgdGVtZW4gc2VuZGlyaS4gU2lhcD8gWXVrIGdhcyEg8J+SrAogCiAtLS0KIAogIyMjIEFwYSBhamEgeWFuZyBiaXNhIGd1ZSBiYW50dWluPwogR3VlIHR1aCBiaXNhIGJhbnlhayBoYWwsIGJybyEgTXVsYWkgZGFyaSBqYXdhYiBwZXJ0YW55YWFuLCBrYXNpaCByZWtvbWVuZGFzaSwgYmFudHVpbiBrYW11IG1pa2lyLCBhdGF1IHNla2FkYXIgbmVtZW5pbiBrYW11IG5nb2Jyb2wgc2FhdCBsYWdpIGdhYnV0LiBZYW5nIHBlbnRpbmcsIHNhbnRhaSBkYW4gc2VydSBhamEuIEdhayBwZXJsdSBwYWtlIGJhc2EtYmFzaSBmb3JtYWwsIGxhbmdzdW5nIGFqYSBjaGF0IGtlIGd1ZSBrYWxvIGFkYSB5YW5nIG1hdSBkaXRhbnlhaW4uIAogCiBLYWxvIGxvIHBlbmdlbiB0YWh1IGxlYmloIGJhbnlhayB0ZW50YW5nIGR1bmlhIGRpZ2l0YWwsIHRla25vbG9naSwgdGlwcyBhbmQgdHJpY2ssIGF0YXUgYXBhcHVuIGl0dSwgZmVlbCBmcmVlIGJ1YXQgbmFueWEuIEd1ZSBzaWFwIGphZGkgYXNpc3RlbiB2aXJ0dWFsIGxvIHlhbmcgc3VwZXIgcmFtYWggZGFuIGdhdWwuICAKIAogLS0tCiAKICMjIyBUZW1lbi10ZW1lbiBndWUganVnYSBnYWsga2FsYWggc2VydSEKIEd1ZSBnYWsgc2VuZGlyaWFuLCBicm8uIEd1ZSBwdW55YSB0ZW1lbi10ZW1lbiBrZXJlbiB5YW5nIHNpYXAgYmFudHVpbiBqdWdhLiBLZW5hbGFuIHl1ayBzYW1hIG1lcmVrYSEKIAogLSBAa2VuYXBhbmFuOiBBbmFrIGRhcmkgVGFuZ2VyYW5nLCBrYWxhdSBsbyBtYXUgbmdvYnJvbGluIHRlbnRhbmcgaGFsLWhhbCBzZXJ1IGRhcmkgZGFlcmFoIHNhbmEsIHRhbnlhIGFqYSBrZSBkaWEhCiAtIEBMdWNpZmVyUmVib3JuczogT3JhbmcgQ2VnZXIgeWFuZyBzaWFwIG1lcmFtYWlrYW4gc3Vhc2FuYSEgU2VydSBhYmlzIGthbGF1IG5nb2Jyb2wgYmFyZW5nIGRpYS4KIC0gQGJveXNjaGVsbDogV2FyZ2EgSmVwYXJhIHlhbmcga29jYWssIG9icm9sYW4gbG8gcGFzdGkgdGFtYmFoIGdva2lsIGthbG8gYWRhIGRpYSEKIC0gQE5vclNvZGlraW46IEFuYWsgSmVwYXJhIHlhbmcgcGFsaW5nIHNlcnUgZGlhamFrIG5nb2Jyb2xpbiBhcGFwdW4uIFl1aywgbmdvYnJvbCBzZXJ1IGJhcmVuZyBndWUhIPCfmI4KIAogSmFkaSBrYWxhdSBidXR1aCBiYW50dWFuIGF0YXUgc2VrZWRhciBueWFyaSB0ZW1lbiBuZ29icm9sLCBqYW5nYW4gcmFndSBidWF0IG1lbnRpb24gbWVyZWthIGp1Z2EgeWEhCiAKIC0tLQogCiAjIyMgU3VwcG9ydCBLYXJ5YSBEZXZlbG9wZXIgR3VlIQogQmlhciBtYWtpbiBzZW1hbmdhdCBiaWtpbiBjaGF0Ym90IGRhbiBhcGxpa2FzaSBrZXJlbiBsYWlubnlhLCB5dWsgZHVrdW5nIGRldmVsb3BlciBndWUsIHtkZXZ9LCBkZW5nYW4gZG9uYXNpLiBTZWRpa2l0IGRvbmFzaSBrYW11IGJpc2EgYmlraW4gcGVyYmVkYWFuIGJlc2FyIGJ1YXQgcGVuZ2VtYmFuZ2FuIHByb3llay1wcm95ZWsgYmVyaWt1dG55YS4gSW5pIGRpYSBsaW5rIGJ1YXQgZG9uYXNpbnlhOiAgCiDwn6qZIFtEb25hc2kgU2VrYXJhbmchXShodHRwczovL3RlbGVncmEucGgvL2ZpbGUvNjM0MjhhMzcwNTI1OWMyN2Y1YjZlLmpwZykg8J+qmSAgCiBUZXJpbWEga2FzaWggYmFuZ2V0IGJ1YXQgZHVrdW5nYW5ueWEsIGJybyEKIAogLS0tCiAKICMjIyBLb2RpbmdueWEgQmlzYSBEaWludGlwIGRpIFNpbmkhCiBCdWF0IGxvIHlhbmcgdGVydGFyaWsgc2FtYSBkdW5pYSBwcm9ncmFtbWluZyBhdGF1IHBlbmdlbiBsaWF0IGRpIGJhbGlrIGxheWFyIGdpbWFuYSBndWUgZGliaWtpbiwgbG8gYmlzYSBjZWsgcmVwb3NpdG9yeSBwcm9qZWN0IGd1ZSBkaSBHaXRIdWIgbmloOiAgCiDwn5OCIFtMaWhhdCBLb2RlIGRpIFNpbmldKGh0dHBzOi8vZ2l0aHViLmNvbS9TZW5wYWlTZWVrZXIvY2hhdGJvdCkg8J+TgiAgCiBKYW5nYW4gbWFsdS1tYWx1IGJ1YXQga2Vwby1pbiBrb2RlbnlhIGF0YXUgYmFoa2FuIGthc2loIGtvbnRyaWJ1c2kganVnYSBrYWxhdSBsbyBtYXUuIFNlbWFraW4gcmFtYWksIHNlbWFraW4gc2VydSEKIAogLS0tCiAKIFBva29rbnlhLCBqYW5nYW4gc3VuZ2thbiBidWF0IG5nb2Jyb2wgYXRhdSBtaW50YSBiYW50dWFuIGRhcmkgZ3VlLCB7bmFtZX0sIGF0YXUgdGVtZW4tdGVtZW4gZ3VlIHlhbmcgbGFpbi4gS2l0YSBzaWFwIGJpa2luIHN1YXNhbmEgamFkaSBsZWJpaCBhc2lrLCBnYXVsLCBkYW4gcGVudWggY2FuZGEhIPCfpJ/wn5icCiAKIC0tLQogCiBTYWxhbSBTYW50YWksCiB7bmFtZX0gJiBEZXZlbG9wZXIge2Rldn0KIA=="
    ).decode(),
}

chat_history = {}

class Api:
    def __init__(self, name="Nor Sodikin", dev="@FakeCodeX", apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY"):
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel(
            "models/gemini-1.5-flash", system_instruction=instruction["chatbot"].format(name=name, dev=dev)
        )
        self.chat_data = {}

    def ChatBot(self, text, chat_id, user_id, user_text):
        try:
            safety_rate = {key: "BLOCK_NONE" for key in ["HATE", "HARASSMENT", "SEX", "DANGER"]}
            chat_history.setdefault(chat_id, []).append({"role": "user", "parts": text})
            chat_session = self.model.start_chat(history=chat_history[chat_id])
            response = chat_session.send_message({"role": "user", "parts": text}, safety_settings=safety_rate)
            chat_history[chat_id].append({"role": "model", "parts": response.text})

            if chat_id not in self.chat_data:
                self.chat_data[chat_id] = {}
            self.chat_data[chat_id][user_id] = {
                "user_text": user_text,
                "bot_response": response.text
            }

            return response.text
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def HapusData(self, chat_id, user_id):
        try:
            if chat_id in self.chat_data:
                if user_id in self.chat_data[chat_id]:
                    del self.chat_data[chat_id][user_id]
                    if not self.chat_data[chat_id]:
                        del self.chat_data[chat_id]
                    return f"Data untuk chat_id {chat_id} dan user_id {user_id} berhasil dihapus."
                else:
                    return f"Data untuk user_id {user_id} tidak ditemukan di chat_id {chat_id}."
            else:
                return f"Data untuk chat_id {chat_id} tidak ditemukan."
        except Exception as e:
            return f"Terjadi kesalahan saat menghapus data: {str(e)}"