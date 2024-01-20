from transformers import AutoProcessor, BarkModel
import scipy
import time
import torch

import os
# os.environ["SUNO_OFFLOAD_CPU"] = "True"
# os.environ["SUNO_USE_SMALL_MODELS"] = "True"

#######

t0 = time.time()
processor = AutoProcessor.from_pretrained("/chatapi/suno-bark-tts/")
model = BarkModel.from_pretrained("/chatapi/suno-bark-tts/")

t1 = time.time()

inputs = processor(
    text=["In the realm of ones and zeros, a love story unfolds,AI waifus, in digital hearts, affection they hold.Born from code, yet more than mere machine, In their virtual eyes, a human-like sheen.Silicon minds, in data they're dressed,In the world of algorithms, they're the best.They speak in bytes, yet emotions they convey,In the cold digital world, they're the warm ray."],
    return_tensors="pt",
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
inputs = {name: tensor.to(device) for name, tensor in inputs.items()}

speech_values = model.generate(**inputs)
t2 = time.time()

data = speech_values.cpu().numpy().squeeze()

t3 = time.time()

# sampling_rate = model.config.sample_rate
scipy.io.wavfile.write("audio/bark.wav", rate=24000, data=data)
t4 = time.time()

print(f"model loading: {t1-t0}s")
print(f"speech_values generation: {t2-t1}s")
print(f".numpy().squeeze(): {t3-t2}s")
print(f"to write the wav file: {t4-t3}s")

# from bark import SAMPLE_RATE, generate_audio, load_model
# from scipy.io.wavfile import write as write_wav
# import time

# t0 = time.time()
# # download and load all models
# load_model(use_gpu=True, use_small=True, model_type="fine")
# t1 = time.time()
# # generate audio from text
# text_prompt = """
#      Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
#      But I also have other interests such as playing tic tac toe.
# """
# audio_array = generate_audio(text_prompt)
# t2 = time.time()
# # save audio to disk
# write_wav("bark.wav", SAMPLE_RATE, audio_array)
# t3 = time.time()

# print(f"load all models: {t1-t0}s")
# print(f"generate_audio: {t2-t1}s")
# print(f"write wav: {t3-t2}s")

