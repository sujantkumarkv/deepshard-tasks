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
