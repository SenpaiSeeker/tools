import google.generativeai as genai


class ChatBot:
    def __init__(
        self,
        name="Tomi",
        dev="@NorSodikin",
        apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY",
        intruction=(
            "Hei, lo ini kayak temen nongkrong yang paham banget soal semua hal kekinian dan bahasa slang. "
            "Job desk lo adalah ngejelasin apapun yang lo dapet dari input orang lain, dengan gaya bahasa yang asik dan lucu. "
            "Ga perlu terlalu serius, yang penting gokil dan ngena. Deskripsinya harus singkat, jelas, dan ga lebih dari 3500 karakter. "
            "Lo bisa pakai bahasa dari list ini: "
            "1. Anak gaul "
            "2. Gaul abis "
            "3. Kekinian "
            "4. Santuy "
            "5. Keren parah "
        ),
    ):
        self.intruction = intruction + f"Dan nama lo adalah {name}. serta developer, pencipta, dev, pembuat lo adalah: {dev}"
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=self.intruction)

    def Text(self, text):
        try:
            response = self.model.generate_content(text)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
