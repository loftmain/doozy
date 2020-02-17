FROM continuumio/miniconda3:latest

MAINTAINER   Lee, Jinjae <loftmain@gmail.com>

ARG	DOOZY_REF

ENV	DOOZY_REF ${DOOZY_REF:-master}

RUN apt-get update && \
	apt-get autoclean && \
	apt-get install -y --no-install-recommends \
	qtbase5-dev-tools \
	curl \
	xvfb \
	libegl1-mesa \
	gfortran \
	x11-xserver-utils \
	libxkbcommon-x11-0 \
	git \
	x11-utils

RUN git clone \
	--single-branch \
	--branch $DOOZY_REF \
	https://github.com/loftmain/doozy.git /src/doozy.git

RUN conda env create -f /src/doozy.git/setup/environment.yml

ENV PATH /opt/conda/envs/doozy_env/bin:$PATH

RUN mv /src/doozy.git/setup/benchmarks.py /opt/conda/envs/doozy_env/lib/python3.5/site-packages/zipline/data && \
		mv /src/doozy.git/setup/loader.py /opt/conda/envs/doozy_env/lib/python3.5/site-packages/zipline/data

SHELL ["bin/bash", "--login", "-c"]

# Initialize conda in bash config files:
RUN conda init bash

# Activate the environment
RUN echo "conda activate doozy_env" > ~/.bashrc

CMD ["python", "/src/doozy.git/src/run.py"]
