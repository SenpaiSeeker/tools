import requests

API_KEY = "AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY"


class Chat:
    def gemini(self, question):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={API_KEY}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": question}]}],
            "generationConfig": {
                "temperature": 1,
                "topK": 0,
                "topP": 0.95,
                "maxOutputTokens": 8192,
                "stopSequences": [],
            },
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return (
            response.json()["candidates"][0]["content"]["parts"][0]["text"]
            if response.status_code == 200
            else f"Failed to generate content. Status code: {response.status_code}"
        )
