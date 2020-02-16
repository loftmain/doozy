FROM continuumio/miniconda3:latest

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

ARG	DOOZY_REF

ENV	DOOZY_REF ${DOOZY_REF:-master}

RUN git clone \
	--single-branch \
	--branch $DOOZY_REF \
	https://github.com/loftmain/doozy.git /src/doozy.git


#ADD ~/docker/enviroment.yml /tmp/environment.yml

RUN conda env create -f /src/doozy.git/setup/environment.yml

ENV PATH /opt/conda/envs/doozy_env/bin:$PATH

SHELL ["/bin/bash", "-c"]

CMD ["bin/bash"]

