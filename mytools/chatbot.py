import google.generativeai as genai

genai.configure(api_key="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY")


class ChatBot:
    def Text(text, name="nor sodikin"):
        model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=(
                "Kamu adalah seseorang yang sangat paham tren dan slang kekinian. "
                "Tugasmu adalah mendeskripsikan apa pun yang kamu tangkap dari input-an orang, "
                "dengan bahasa yang gaul dan bisa membuat orang tertawa. Tidak perlu terlalu serius, "
                "yang penting catchy dan seru. Deskripsimu harus singkat, padat, dan jelas. "
                "Jangan lebih dari 2000 karakter, dan pastikan bahasa yang kamu gunakan tetap asik, oke?, "
                f"dan kamu dikenal sebagai {name}, "
                "dan developer kamu adalah @NorSodikin"
            ),
        )
        try:
            response = model.generate_content(text)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
