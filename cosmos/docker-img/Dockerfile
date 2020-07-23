FROM ubuntu:18.04

ENV TIMEZONE=America/Los_Angeles
ENV COSMOS_REPO https://github.com/oresat/uniclogs-software
ENV COSMOS_BRANCH capstone-dev
ENV COSMOS_VERSION 4.4.2
ENV DART_HOST localhost
ENV DART_PORT 5432
ARG DART_DB
ARG DART_USERNAME
ARG DART_PASSWORD

RUN ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
RUN apt-get update && apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -qqy \
  cmake \
  curl \
  freeglut3 \
  freeglut3-dev \
  gcc \
  git \
  g++ \
  git \
  gnome-terminal \
  iproute2 \
  libffi-dev \
  libgdbm-dev \
  libgdbm5 \
  libgstreamer-plugins-base1.0-dev \
  libgstreamer1.0-dev \
  libncurses5-dev \
  libpq-dev \
  libreadline6-dev \
  libsmokeqt4-dev \
  libssl-dev \
  libyaml-dev \
  net-tools \
  nodejs \
  postgresql \
  python-psycopg2 \
  qt4-default \
  qt4-dev-tools \
  ruby2.5 \
  ruby2.5-dev \
  vim \
  x11-apps \
  zlib1g-dev

RUN gem install rake --no-document
RUN gem install bundle --no-document

RUN git clone ${COSMOS_REPO} /opt/
WORKDIR /opt
RUN git checkout ${COSMOS_BRANCH}
RUN mv /opt/cosmos /
RUN rm -rf /opt/*
RUN mv /cosmos /opt
WORKDIR /opt/cosmos
RUN bundle install --clean --deployment
