from fastapi import FastAPI, Response
from model import Model
# import subprocess, pyaudio, sys, wave
from pydantic import BaseModel
from transcribe import Transcribe
import json

# Define the payload structure for the API
class Payload(BaseModel):
    prompt: str = None
    filepath: str = None

# Load the configuration from the JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize the FastAPI app
app = FastAPI()

# Load the transcribe configuration and initialize the transcriber
transcribe_config = config['transcribe']
transcriber = Transcribe(cwd=transcribe_config['cwd'], 
                        audio_file_name=transcribe_config['audio_file_name'], 
                        model=transcribe_config['model'])

# Initialize the model and the chatModule
app = FastAPI()
model = Model()
chatmodule, StreamToStdout = model.model_pipeline()

# Define the main API endpoint
@app.post("/{mode}")
async def root(mode: str, payload: Payload):
    """
    Main API endpoint that handles diff input & output modes for user.

    This endpoint accepts a POST request with a payload based on the `Payload(BaseModel)` type.

    Args:
        mode (str): The mode of operation. Can be either "t2t" for text-to-text or "v2t" for voice-to-text.
        payload (Payload): The payload containing either a text prompt or a filepath to an audio file.

    Returns:
        dict: If the mode is valid, returns a dictionary with the generated output and stats. 
              If the mode is invalid, returns a dictionary with an error message.
    """
    # If the mode is t2t or v2t, generate response for prompt or transcribe the audio
    if mode == "t2t" or mode == "v2t":
        prompt = payload.prompt if payload.prompt else (transcriber.transcribe(payload.filepath) if payload.filepath else None)
        output = chatmodule.generate(prompt=prompt, progress_callback=StreamToStdout(callback_interval=2))
        stats = chatmodule.stats()
        return Response(f"output: {output} \nstats: {stats}", media_type="text/event-stream")
    else:
        return {"error": "No mode or Invalid mode..."}



"""
### this is earlier code trying to use whisper.cpp's `stream` and pyaudio 
# but since i don't have access to jetson's microphone, 
# trying to send over audio files from mac to device.


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "pytest.wav"
MIC_INDEX = 11

stream = p.open(format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE)
process = subprocess.Popen(
    ['./stream', '-m', './models/ggml-base.en.bin', '-t', '8', '--step', '500', '--length', '5000'],
    cwd='../opt/whisper.cpp',
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
while True:
    try:
        data = stream.read(CHUNK_SIZE)
        process.stdin.write(data)
        output = process.stdout.read(1)
        if output == b'':
            break
        sys.stdout.buffer.write(output)
    except KeyboardInterrupt:
        break

stream.stop_stream()
stream.close()
p.terminate()
process.terminate()

# return model_pipeline(prompt=prompt)


audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS, input_device_index=MIC_INDEX,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

print(stream)
print ("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow = False)
    print(data)
    frames.append(data)
print ("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

"""