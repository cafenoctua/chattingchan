FROM nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    vim

WORKDIR /opt
RUN wget https://repo.continuum.io/archive/Anaconda3-2019.10-Linux-x86_64.sh && \
    sh Anaconda3-2019.10-Linux-x86_64.sh -b -p /opt/anaconda3 && \
    rm -f Anaconda3-2019.10-Linux-x86_64.sh

ENV PATH /opt/anaconda3/bin:$PATH

RUN pip install --upgrade pip && pip install \
    keras==2.3 \
    scipy==1.4.1 \
    tensorflow-gpu==2.1
WORKDIR /

RUN sudo apt install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    swig

RUN pip3 install mecab-python3==0.996.5

RUN pip install torch==1.6.0 torchvision==0.7.0
# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--LabApp.token=''"]