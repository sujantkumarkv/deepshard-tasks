from mlc_chat import ChatModule
from mlc_chat.callback import StreamToStdout
import json
"""
This module is for setting up the model and a pipeline for generating responses.
It uses the `mlc_chat` to create a `ChatModule` instance and load the model in the config file.
The `model_pipeline` function is the main entry point to interact with the chat model.
"""

# Load the configuration file
with open('config.json', 'r') as f:
   config = json.load(f)

class Model:
   def __init__(self):
      self.model=config['chat']['model'] # or "dist/Llama-2-7b-chat-hf-q4f16_1-MLC"
      self.model_lib_path=config['chat']['model_lib_path']

   def model_pipeline(self):
      """
      This function provides a pipeline for generating responses using the chatModule instance.

      It currently returns the ChatModule instance directly, but can be extended to generate a response for a given prompt,
      and return additional statistics about the model's performance.
      uncomment to enable it in this file itself, but currently its used to generate in main.py

      Returns:
         ChatModule: The ChatModule instance & the streaming instance.
      """
      # Generate a response for a given prompt
      #  output = str(cm.generate(prompt=prompt, progress_callback=StreamToStdout(callback_interval=2)))
      #  stats = cm.stats()
      #  return {"output": output, "stats": stats}
      
      # For now, returning the ChatModule instance directly
      # Create a ChatModule instance using the model and library path
      cm = ChatModule(model=self.model, model_lib_path=self.model_lib_path)
      return (cm, StreamToStdout)