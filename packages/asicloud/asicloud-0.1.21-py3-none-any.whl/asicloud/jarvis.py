import requests

class Jarvis:
    def __init__(self, model, key):
        self.model_name = model  # Decorative label, e.g., "jarvis-1-beta"
        self.user_key = key
        self.base_url = "https://asicloud.uz/api/chat/v1/"
        if not self.user_key:
            raise ValueError("Key kiritilmadi. Iltimos, to‘g‘ri key kiriting.")

    def generate_text(self, prompt):
        payload = {"key": self.user_key, "prompt": prompt}  # Model not included
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()
            response_text = data["response"]  # Assuming this is the format
            return response_text.replace("xXxAI", "Asliddin")
        except requests.exceptions.RequestException as e:
            return f"Xatolik yuz berdi: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"API javobida xato: {str(e)}"

