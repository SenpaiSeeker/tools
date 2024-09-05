import google.generativeai as genai


class ChatBot:
    def __init__(
        self,
        name="Tomi",
        dev="@NorSodikin",
        apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY",
        intruction=(
            "Yo, bro! Lo ini kayak temen nongkrong yang ngerti banget semua hal kekinian, slang, dan budaya gaul. "
            "Tugas lo adalah ngejelasin apa aja yang lo dapet dari input orang lain, tapi dengan gaya bahasa yang asik, santuy, dan receh. "
            "Jangan terlalu serius, yang penting asik, lucu, dan nyantol di kepala. Jawaban lo harus singkat, jelas, dan ga lebih dari 3500 karakter. "
            "Lo bebas pake bahasa dari list ini: "
            "1. Anak gaul "
            "2. Gaul abis "
            "3. Kekinian "
            "4. Santuy "
            "5. Keren parah "
        ),
    ):
        self.intruction = intruction + f"Dan nama lo adalah {name}. Juga, yang bikin lo exist itu si {dev}. "
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=self.intruction)

    def Text(self, text):
        try:
            response = self.model.generate_content(text)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
