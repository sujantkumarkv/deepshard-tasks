# llama-inference
task to optimize for tokens/sec inferencing for llama.

I'll log my approach + progress here as in steps on how to go about it in the README. I think this'll also serve to see how i do things and how can I improve it based on feedback.
I may write something wrong, and may correct on it in the latter logs.

### log#1
- Based on what I know, I can do inference with many libraries: vLLM, TGI, llama.cpp, gpt-fast etc..
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


### log#5
- wrote script to with most vanilla approach in `llama-inference/speed.py` and ~6 tokens/s (sometimes 5.9, 6.2 and so on)
 ![Screenshot 2023-12-25 at 7 26 16 AM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/683faa5a-4d13-4ede-9feb-643ed1f65263)

_note: i made mistake here & calculated wrong. also, using only cpu, it takes looong time to run (not feasible)_

- also read this [blog](https://vgel.me/posts/faster-inference/). Multi-query attention is already baked in llama arch, i was under assumption we can tweak these for inference (earlier had idea to use GQA or Group Query attention, but we can't)
  

### log#6
- okay so i'm getting a lott of those nasty system errors while getting installing/setting up on all methods i'm trying.
- I cloned & build `llama.cpp` and something is really wrong here on the lower cuda & arch level because the original unquantized model showed OOM error, so i downloaded `Q8_0`, `Q6_K`, `Q4_K_M` & even `Q4_0` gguf files but it still gives error.
  
  ![Screenshot 2023-12-26 at 3 56 23 AM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/e28f8c01-3e4d-4207-9b9c-2c04e481637d)
  ![Screenshot 2023-12-26 at 3 57 09 AM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/be321831-675d-41f4-89be-d5a684bb57ca)

- I moved on to another way as i remember a tweet that `ctransformers` (python bindings using GGML library in C/C++) works great; i pip install it but it gives error about `libctransformers.so`. I then found the file, it exists and made it executable but it doesn't work. 
  ![Screenshot 2023-12-26 at 7 05 25 PM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/dc563256-2cb6-4c27-aa00-7031ab5dca3a)
  
- The doc also suggested to download `ctransformers[cuda]` which prompts to install `nvidia-pyindex` and `nvidia-cublas-cu12`. The former worked but the later gave the following error:
  ![image](https://github.com/sujantkumarkv/llama-inference/assets/73742938/298582af-9959-4b7a-8daf-8d89fc16ab04)

- I then tried to use `torch.compile` (spins custom kernels to boost inference) for the first approach which gave ~6 tokens/s, but triton was missing but `pip install triton` didn't work (idk)
![Screenshot 2023-12-26 at 6 49 11 PM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/4d785650-1c34-4671-a631-07252884a026)

and then i tried to build from source like so from its docs but it gave errors, and the build fails giving the reason for failure in a `subprocess` and *not able to build wheel files*.
![Screenshot 2023-12-26 at 6 49 55 PM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/e801ea51-1c63-4db0-875c-0ec537cbda55)


### log#7
- I tried vLLM, again installing via pip or building from source gave some cuda related error (*it works on colab though, also this may not be worth now bcz it doesn't support quantization properly, only AWQ as of now (those are optimized for 4 bits mostly)*)
  *(note: I was running this inside the container i made & launched which contaied pytorch, python, cuda, llama.cpp, transformers)*
![Screenshot 2023-12-27 at 8 33 43 PM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/07cae686-901b-48df-9b4e-baee58c71a27)

- fast-gpt is raw pytorch implementation, read [this blog](https://pytorch.org/blog/accelerating-generative-ai-2/) on it. It uses various methods like `torch.compile` (which i tried earlier), `int8 quantization` and static kv-caching. Will try this again but its not a library, so need to dissect its files to suit my needs.

- I finally tried going the simple *jetson container tutorials* by using `text-generation-webui` image, loaded `Q8_0.gguf` model with `llama.cpp` and **finally this worked** 😊 *(so this tells about some low-level error i need to fix bcz this worked)*
so I get barely ~3.5 tokens/s.
  
![Screenshot 2023-12-27 at 7 56 31 PM](https://github.com/sujantkumarkv/llama-inference/assets/73742938/40123cd8-c535-4c9e-ace0-be5380bcc60b)

I read on `r/localLlama` about optimizing this and probably the `-t N` parameter in `llama.cpp` is best equal to the number of vCPUs (eg. it was 7 for him). I tried finding it for our device (help me if you have detailed specs)

- I also found about `ctranslate2`, so will try that now. Also `fast-gpt` is most exciting bcz its raw just raw pytorch (will need to look at its code properly, so later)


  


  

