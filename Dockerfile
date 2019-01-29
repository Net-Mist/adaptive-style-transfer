FROM tensorflow/tensorflow:1.12.0-gpu-py3

RUN apt update \
    && apt install -y --no-install-recommends \
    libsm6 libxrandr2 libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install fire tqdm opencv-python
WORKDIR /root/workspace
CMD bash

