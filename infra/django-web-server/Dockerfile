FROM ubuntu:18.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV HOME /root
ENV PATH $HOME/miniconda/bin:$PATH
ENV APP_PATH /usr/src/app

RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
    software-properties-common

# -- Install Python dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yqq --no-install-recommends \
    build-essential \
    python3.7 \
    python3-pip \
    git \
    wget \
    vim \
    postgresql \
  && apt-get -q clean

# -- Install Application into container:
RUN set -ex && mkdir -p ${APP_PATH}/backend

WORKDIR ${APP_PATH}

# -- Adding requirement files
COPY src/backend/environment.yml src/backend/environment.yml
COPY infra/scripts/setup-server.sh infra/scripts/setup-server.sh

# -- Install dependencies:
RUN infra/scripts/setup-server.sh