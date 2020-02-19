FROM continuumio/miniconda3:latest

MAINTAINER   Lee, Jinjae <loftmain@gmail.com>

ARG	DOOZY_REF

ENV	DOOZY_REF ${DOOZY_REF:-master}

# install x11, git ...
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
	x11-utils \
	fonts-nanum-coding && \
	apt-get clean && \
	rm -rf /var/cache/apk/*

RUN git clone \
	--single-branch \
	--branch $DOOZY_REF \
	https://github.com/loftmain/doozy.git /src/doozy.git

# make conda env
RUN conda env create -f /src/doozy.git/setup/environment.yml

# activate conda env
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

# change zipline source code
RUN mv /src/doozy.git/setup/benchmarks.py /opt/conda/envs/env/lib/python3.5/site-packages/zipline/data && \
		mv /src/doozy.git/setup/loader.py /opt/conda/envs/env/lib/python3.5/site-packages/zipline/data

# default running program
CMD ["conda", "run", "-n", "env", "python", "/src/doozy.git/src/run.py"]
