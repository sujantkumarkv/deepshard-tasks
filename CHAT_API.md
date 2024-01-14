# Chat API
```
### Technical Challenge
#### Overview 
In this technical challenge, you are going to use what you have learned about the Jetson Orin to build a simple LLM API. 
The API is going to be used to provide real-time chat to a user, with a caveat — it is voice based. 
This means that you are going to have to integrate whisper within your API, to parse user commands, and successfully generate a response back. The response can be one of two types: 
1. The AI responding back via voice 
2. A simple textual response 
To do this, you will need the following: 
1. Whisper, running on the Jetson locally itself: 
2. MLC AI running the core API on the Orin:  
3. Jetson containers 
4. Text to speech model → This will allow the AI to respond as voice instead of text.
   
#### Requirements 
1. The API should have a endpoint that I can send a POST request to, in order to generate a completion 
2. This endpoint should accept a prompt in either text, or WAV file format
3. This endpoint should also allow the user to specify whether they want to receive back voice, or text 
a. If user wants to receive text, process the prompt with a model, and return text 
b. If the user wants to receive voice, process the prompt with a model, convert the processed text into voice using Coqui, and then return back the WAV file
 
To summarize, there will be 4 possible cases: 
* User sends text, wants to receive back text 
* User sends voice, wants to receive back text 
* User sends text, wants to receive back voice 
* User sends voice wants to receive back voice 
Your API should handle each of these cases gracefully. You must also think of possible edge cases where the input is out-of-format, or handle any associated errors without crashing. 
For the LLM running on the Jetson, you can use base Mistral-instruct-7B model. This model is built to follow instructions, and so can handle your requests well in most cases.

#### Completion criteria 
A successful implementation will be judge upon the following criteria:
1. Correctness: Does your code work for all 4 cases? 
2. Code quality: Is your code documented, easy to understand, and clean?
3. Efficiency: Is your code performant?
```
i'll try logging my problems & progress here.

### log#1

- spent time in reading code on to build APIs, compatible with the architecture, server features, good with models etc.
- read about ASGI, server configs, flask, fastAPI, caching logic, then ray which was a great fit (even alibaba, tiktok uses it in production)
- didn't set `--volume` for the docker container `mlc:r36.2.0-mlc`, and lost some changes i did... i set up `chat_api`, changed the `jetson-containers/run.sh` to include it during launch. 

![image](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/26283316-46b6-4a9e-b444-f413186c2a64)

- wrote `server.py` in the `/opt/chat_api` directory for testing server, **it runs** but gave errors in not running in the background for persistent requests & responses as i tried curl in different terminal session.
  
### log#2

- the plan is to have a script which would start an API serving requests in a chat format.
- I'm running everything inside the container and i was facing issues in getting `mlc_chat` (python api) to work, `mlc_chat_cli` worked though. I then try to build `mlc-llm` from scratch, but i got errors where it wasn't able to find something called `tvm` but it was present in `3rdparty/tvm` in the `mlc-llm` so i exported for it to able to find it `export PYTHONPATH=/opt/mlc-llm/3rdparty/tvm/python:$PYTHONPATH` and this worked.
- but then it wasn't able to find some files (as shown), I tried copying it to destination directories, but it doesn't work.
  
![image](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/610ccf28-0ee3-4354-8543-acfbe703cdfb)

- probably the problem was the virtual env `venv` i was using inside the container (container is already isolated). when using the image which had mlc installed, `mlc_chat` worked.
- Then, the issue was with the mistral's format since mlc requires a certain format of model being compiled for it to run. [Here's the page](https://llm.mlc.ai/docs/compilation/compile_models.html) on compiling the models. I did all the steps and it still threw error as shown:

![image](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/598ab4d7-3de7-4df6-b1bb-9107e0b774cc)
  
- On further reading on it, **_the issue was that the compiled model binary libs (in the form of `xyz.so` `abc.tar` `pqr.dll`) for different platform, the Mistral one was only compiled for `x86` architecture and not for `aarch64` as our jetson device_**, so I downloaded the `abcxyz-MLC` quantized file and then compiled it to get the `abcxyz-cuda.so` file. `mlc_chat` then worked with an approx `27 tokens/s`

![image](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/f4226c10-2f82-49b1-99ad-ddfe3d142508)

### log#3

- Wasted a lot of time in using ray's REST server, it gave slow initialization errors, then saw I could use `mlc_chat.rest`'s REST server
- running the `mlc_chat.rest` server, and POST requests, it works :)

  <img width="733" alt="image" src="https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/8f47b978-a39f-4a90-9fae-3e3c57d6ed82">

- then, compiled & made whisper.cpp from source. The issue was to get *just* the text output as it outputs system and many other details to console.
- The option to save it to a text file also exists with `--output-txt` flag, so i tried to change the `whisper.cpp` c++ code itself to supress output and give text and stats, that was a wasted effort.
- I tried `suprocess` for python scipt and the hack I used was to not `capture_output` which sets the `stdout` and `stderr` from `subprocess.run` to `PIPE`, read [here](https://docs.python.org/3/library/subprocess.html#subprocess.run) and the parse the console output `stdout.output.decode('utf-8')` and then extract the text out of there, it works.
  
![Screenshot 2024-01-08 at 12 44 10 PM](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/8cf74bdf-ea3d-4856-950c-ff5f6ca3563e)

- then I implemented two options, Text2Text and Voice2Text in a script (code optimizations later)


### log#4

- Not having much experience with docker before (tried my best avoiding it lol), one mistake i did was trying to get libraries build during a running container. now, i lost changes after it stopped. Also, the task required me to craft the API itself with live audio transcribing than how I did currently (miscommunication)
- spent a hell lotta time to read all the scripts in jetson-containers, their build process, arguments, different dependencies (since its jetson device with a different architecture, eg. the Dockerfile installs `llvm` etc for the aarch64)
- i started with the thought to replicate the entire build environement locally first in the host machine (jetson orin) and then at the end dockerize it with a custom Dockerfile by combining all the steps from all those individual dockerfiles (pytorch, python etc), but its not just a `pip install transformers` for libraries due to arch difference & there's a lot of steps in their respective dockerfiles in `jetson-containers/packages/*` and its a pain, so i'm going with (as of now) to use a built image, add custom libraries on top with a new Dockerfile, and have my chatapi's code in the image, i guess i can iterate faster as i'll mount it with `--volume`.
- There's a lot of ubuntu/docker nuances i haven't worked with, and just saw how the BASE_IMAGE used in the official Dockerfile for libs in `jetson-containers/packages/*` worked in `jetson-containers/jetson_containers/container.py` and need to take all such nuances into account to get it started.

### log#5

- its needed to build stuff almost from scratch again, as to write the new API including whisper, TTS etc.
- built a new image (`chatapi:v0`) on existing `mlc:r36.2.0` with `fastapi` & `uvicorn` with a new Dockerfile.
- ran & tested it with "hello world", works :)
  ![image](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/2bf6146a-7208-4cd8-b54b-74759061c82e)

- running inference with `mlc_chat` sample, works.

  ![image](https://github.com/sujantkumarkv/deepshard-tasks/assets/73742938/4643d0a1-e9e4-44d6-8bc9-7d6404fbe865)

### log#6

- the issue i'm facing with is to make realtime whisper.cpp work. i'm trying to use a `stream` (more, [here](https://github.com/ggerganov/whisper.cpp/tree/master/examples/stream)) file, the file starts, but doesn't pick up audio.
- Now, there are many issues possible (one thing i'm confused is if i would need code to take audio input from my macbook -> send it to jetson device via ssh or something? OR since i'm SSHed into the device, my audio input if picked up, will be directly captured by the `stream` file.)
- diving into `alsa` `pyaudio` `sounddevice` `wave` and [nvidia help forum](https://forums.developer.nvidia.com/search?q=pyaudio), some leads i found are to `arecord` run in my mac along with `stream` in the container OR run arecord in the container, idk!!!
- one doubt i had is regarding how to write Dockerfile correctly to ensure everything is installed properly & the container READS all the tools & dependencies properly so as to not have any error which doesn't show up but exists in the background. gpt4 helped: "Python packages should be installed in the Python's global site-packages directory (which is done automatically when you use `pip install`), it's typically something like `/usr/local/lib/python3.x/site-packages` for Python 3.x & similar to Python packages, system packages installed with `apt-get install` are available system-wide and their installation is not affected by the `WORKDIR` in dockerfile and your application code should be placed in a directory of your choice (like `/chatapi`)"





