import requests

class Jarvis:
    def __init__(self, key):
        # What should we initialize here?
        self.user_key = key
        self.base_url = "https://asicloud.uz/api/chat/v1/"
        if not self.user_key:
            raise ValueError("Key kiritilmadi. Iltimos, to‘g‘ri key kiriting.")

    def generate_text(self, prompt):
        # How do we structure the request?
        payload = {"key": self.user_key, "prompt": prompt}
        try:
            # What method and parameters do we use?
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()
            # How do we extract the response text?
            response_text = data["response"]  # Or data["choices"][0]["message"]["content"]?
            return response_text.replace("xXxAI", "Asliddin")
        except requests.exceptions.RequestException as e:
            return f"Xatolik yuz berdi: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"API javobida xato: {str(e)}"