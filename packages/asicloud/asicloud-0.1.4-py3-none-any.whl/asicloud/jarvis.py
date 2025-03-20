import requests

class Jarvis:
    def __init__(self, model, key):
        self.model_name = model  # Foydalanuvchi "jarvis-1-beta" kiritadi
        self.user_key = key      # Foydalanuvchi qisqa key kiritadi (masalan, "sjJiw342vqs")
        self.base_url = "https://asicloud.uz/asicloudapirequests/jarvis.php"  # Yangi URL

        # Key majburiy
        if not self.user_key:
            raise ValueError("Key kiritilmadi. Iltimos, to‘g‘ri key kiriting.")

    def generate_text(self, prompt):
        # URL parametrlarini tayyorlash
        params = {
            "key": self.user_key,
            "prompt": prompt
        }

        # API so‘rovini yuborish (GET metodi)
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            # JSON javobni parse qilish
            data = response.json()
            # "content" ni olish
            response_text = data["choices"][0]["message"]["content"]
            # So‘z almashtirish
            response_text = response_text.replace("xXxAI", "Asliddin")
            return response_text
        except requests.exceptions.RequestException as e:
            return f"Xatolik yuz berdi: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"API javobida xato: {str(e)}"