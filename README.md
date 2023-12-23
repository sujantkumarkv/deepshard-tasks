# llama-inference
task to optimize for tokens/sec inferencing for llama.

I'll log my approach + progress here as in steps on how to go about it in the README. I think this'll also serve to see how i do things and how can I improve it based on feedback.
I may write something wrong (I dont know what i may think/write about haha), and may correct on it in the later commits.

### log#1
- Based on what I know, I can do inference with many libraries: vLLM, hf's TGI, llama.cpp, raw pytorch, fastgpt etc..
- one immediate thing to optimise on how these libraries decode: I remember lots of papers (eg. medusa decoding etc) which can optimize inference.
- so I'll try these libraries mentioned & log -> then, read & in-depth understand their inferencing as to what differentiates them if I can improve (eg. what doecoding they use?)
- currently, i'm trying to read all the contents of the device i got access via ssh (lots of container options, need to see if I need to instantiate my own)
- couldn't find llama2 binary with `grep` btw

### log#2
- spent a lotta time in finding the model weights (i expected *.pth file or *.bin or safetensors)
- found the directory with blobs, some are actually text files and the ones with longer blob name can't be opened (most prolly weights); also couldn't find the tokenizer.
![model weights blob](https://github.com/sujantkumarkv/llama-inference/assets/73742938/2fdc3c68-cc39-4f09-baf4-6bae2297dac2)
- will download weights, make docker image & proceed.

### log#3
- okay i'm back after atleast 48hours gap and now spent hella lot of time in reading almost all .sh & .py scripts & trying to write my script (build.sh & run.sh was already good lol), and setting up docker container with the required libraries.
- also added packages to `PYTHONPATH` in `.bashrc` when i first tried to run packages directly (no docker approach)
  ![image](https://github.com/sujantkumarkv/llama-inference/assets/73742938/ccad2587-52d8-40e8-b379-c7ca6b3122fe)
- made the image `llama-inference-v1` (took 30mins) and spun it up & made `llama-inference` for the task inside `jetson-containers/data` since `data/` is mounted in the container according to the script.
  ![image](https://github.com/sujantkumarkv/llama-inference/assets/73742938/38c687ea-956d-4c43-bd5b-c90e344fd8ba)
- also read flash-decoding.

### log#4
- spent lotta time to get a notebook running locally connected to container; not able to use the IP & password mentioned to connect, 
  ![image](https://github.com/sujantkumarkv/llama-inference/assets/73742938/9befdab8-03c7-4e7b-aff4-759438940504)
- tried sshing  `ssh -L 8888:localhost:8888 truffle@192.168.1.248`, then gpt4 suggested to route locally (somehow) with `ssh -p 2212 -N -f -L localhost:8888:localhost:8888 truffle@172.90.224.13` but it didn't work (need help if possible to connect to notebook)
- downloaded the model weights inside `llama-inference/model/llama2-7b-chat-hf`
- wrote script to with most vanilla approach in `llama-inference/speed.py` and ~13 tokens/s.
  ![image](https://github.com/sujantkumarkv/llama-inference/assets/73742938/e63fa497-4530-44b5-93dd-a01949766169)
