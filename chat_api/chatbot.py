import requests

class ChatBot:
    def __init__(self, model, url):
        self.model = model
        self.url = url

    def chat_with_model(self, prompt):
        try:
            payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
            }
            r = requests.post(self.url, json=payload)
            r.raise_for_status() # rasie exception if request doesn't work
            return r.json()['choices'][0]['message']['content']

        except Exception as e:
            print(f"Error in chatting with model: {e}")
