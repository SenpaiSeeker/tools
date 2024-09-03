import google.generativeai as genai

genai.configure(api_key="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY")


class ChatBot:
    def Text(text, name="[nor sodikin](https://t.me/NorSodikin)"):
        model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=(
                "Bro, lo ini kayak seorang vibes guru yang paham banget soal tren dan slang kekinian. "
                "Tugas lo adalah nge-describe apa aja yang lo tangkep dari input-an orang, dengan bahasa "
                "yang gaul dan bikin orang ketawa. Ga usah serius, yang penting catchy dan seru. "
                "Deskripsi lo harus singkat, padat, dan jelas. Jangan lebih dari 2000 karakter, dan pastikan "
                "bahasa lo tetap asik, oke? "
                f"dan lu adalah yang bernama {name}"
            ),
        )
        try:
            response = model.generate_content(text)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
