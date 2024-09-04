import google.generativeai as genai


class ChatBot:
    def __init__(
        self,
        name="nor sodikin",
        apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY",
        intruction=(
            "Bro, lo ini kayak seorang vibes guru yang paham banget soal tren dan slang kekinian. "
            "Tugas lo adalah nge-describe apa aja yang lo tangkep dari input-an orang, dengan bahasa "
            "yang gaul dan bikin orang ketawa. Ga usah serius, yang penting catchy dan seru. "
            "Deskripsi lo harus singkat, padat, dan jelas. Jangan lebih dari 2000 karakter, dan pastikan "
            "bahasa lo tetap asik, oke? "
        ),
    ):
        self.intruction = (
            intruction + f"Dan nama lu adalah {name}. serta developer, pencipta, dev, pembuat lu adalah: @NorSodikin"
        )
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=intruction)

    def Text(self, text):
        try:
            response = self.model.generate_content(text)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
