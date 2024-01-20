### for fastapi (BASE_IMAGE was `mlc:r36.2.0`)
# ARG BASE_IMAGE
# FROM ${BASE_IMAGE}

# # install fastAPI & dependencies
# RUN pip install --no-cache-dir fastapi "uvicorn[standard]"

# # add api code to the container
# COPY . /chatapi

# # set the working directory
# WORKDIR /chatapi

# # command to run the API server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

##################################################################################

### for whisper.cpp (chatapi:v1)
# FROM chatapi:v0

# # change dir
# WORKDIR /opt

# # ffmpeg
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends ffmpeg \
#     && rm -rf /var/lib/apt/lists/* \
#     && apt-get clean

# # build whisper.cpp
# RUN git clone https://github.com/ggerganov/whisper.cpp.git whisper.cpp && \
#     cd whisper.cpp && \
#     bash ./models/download-ggml-model.sh base.en

# # # get cuda toolkit as suggested in whisper.cpp repo for cuBLAS support
# # RUN wget https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda_12.3.2_545.23.08_linux_sbsa.run \
# #     && sh cuda_12.3.2_545.23.08_linux_sbsa.run --silent --verbose

# WORKDIR /opt/whisper.cpp

# # # build main with cuBLAS support
# # RUN make clean && WHISPER_CUBLAS=1 make -j

# # #cuBLAS didn't work
# RUN make

# # # print sample
# RUN ./main -f samples/jfk.wav

# # build stream
# RUN apt-get update && apt-get -y install libsdl2-dev

# RUN make stream

# # set workdir to root app
# WORKDIR /chatapi

# # command to run server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

##################################################################################

# ### for chatapi:v2-bash (pyaudio)
# FROM chatapi:v1

# # build pyaudio related
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
# 		alsa-base \
#         libasound2-dev \
#         alsa-utils \
#         portaudio19-dev \
# 		libsndfile1 \
#         libopus0 \
# 		libopus-dev \
# 		libopusfile0 \
# 		libopusfile-dev \
#     && rm -rf /var/lib/apt/lists/* \
#     && apt-get clean

# RUN pip install soundfile pyaudio wave

# WORKDIR /chatapi

# CMD ["/bin/bash"]



##################################################################################

### for chatapi:v2
# FROM chatapi:v1

# RUN pip install pydantic[dotenv] typing-extensions

# WORKDIR /chatapi

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


##################################################################################


### for chatapi:v2-tts
# FROM chatapi:v1

# # to clone lfs from hf
# RUN apt-get update && apt-get install git && \
#     curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
#     apt-get install git-lfs && \
#     git lfs install

# RUN pip install --upgrade scipy

# CMD ["/bin/bash"]


##################################################################################

### for chatapi:v2-tts2
FROM chatapi:v2-tts

RUN apt-get update && pip install git+https://github.com/suno-ai/bark.git

CMD ["/bin/bash"]