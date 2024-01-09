"""
I tried to make it work, server runs but doesn't work, it gave something called "initialization" errors as it was too slow (or maybe due to aarch64). 
Its used in production by alibaba/tiktok, so its promising.
"""
import requests, ray
from fastapi import FastAPI
from ray import serve
from mlc_chat import ChatModule
from mlc_chat.callback import StreamToStdout


MODEL_PATH = "/opt/chat_api/dist/Mistral-7B-Instruct-v0.2-q4f16_1-MLC"
MODEL_LIB_PATH = "/opt/chat_api/dist/libs/Mistral-7B-Instruct-v0.2-q4f16_1-cuda.so"

app = FastAPI()

@serve.deployment
@serve.ingress(app)
class ChatApiServer:
    def __init__(self):
        # Initialize a chatmodule instance
        self.cm = ChatModule(model=MODEL_PATH, model_lib_path=MODEL_LIB_PATH, device='cpu')
        # Vulkan on Linux: Llama-2-7b-chat-hf-q4f16_1-vulkan.so
        # Metal on macOS: Llama-2-7b-chat-hf-q4f16_1-metal.so
        # Other platforms: Llama-2-7b-chat-hf-q4f16_1-{backend}.{suffix}

    @app.post("/")
    def root(self, prompt: str):
        output = self.cm.generate(prompt=prompt, progress_callback=StreamToStdout(callback_interval=2))
        stats = self.cm.stats()
        return stats


ray.init(ignore_reinit_error=True, include_dashboard=False)
chat_api_app = ChatApiServer.bind()
