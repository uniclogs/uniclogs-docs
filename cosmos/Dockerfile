FROM ubuntu:18.04

# Import all the build arguments and environment variables
ENV TIMEZONE America/Los_Angeles
ENV COSMOS_VERSION 4.4.2
ENV DART_HOST localhost
ENV DART_PORT 5432
ARG DART_DB
ARG DART_USERNAME
ARG DART_PASSWORD

# Set the timezone, do a system update, then save the timezone config
RUN ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
RUN apt-get update && apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Install Ubuntu-based dependencies
RUN apt-get install -qqy apt-utils
RUN apt-get install -qqy cmake
RUN apt-get install -qqy curl
RUN apt-get install -qqy freeglut3
RUN apt-get install -qqy freeglut3-dev
RUN apt-get install -qqy gcc
RUN apt-get install -qqy git
RUN apt-get install -qqy g++
RUN apt-get install -qqy git
RUN apt-get install -qqy iproute2
RUN apt-get install -qqy libffi-dev
RUN apt-get install -qqy libgdbm-dev
RUN apt-get install -qqy libgdbm5
RUN apt-get install -qqy libgstreamer-plugins-base1.0-dev
RUN apt-get install -qqy libgstreamer1.0-dev
RUN apt-get install -qqy libncurses5-dev
RUN apt-get install -qqy libpq-dev
RUN apt-get install -qqy libreadline6-dev
RUN apt-get install -qqy libsmokeqt4-dev
RUN apt-get install -qqy libssl-dev
RUN apt-get install -qqy libyaml-dev
RUN apt-get install -qqy net-tools
RUN apt-get install -qqy nodejs
RUN apt-get install -qqy postgresql
RUN apt-get install -qqy python-psycopg2
RUN apt-get install -qqy qt4-default
RUN apt-get install -qqy qt4-dev-tools
RUN apt-get install -qqy ruby2.5
RUN apt-get install -qqy ruby2.5-dev
RUN apt-get install -qqy vim
RUN apt-get install -qqy zlib1g-dev

# Install Rake and Bundler
RUN gem install rake --no-document
RUN gem install bundle --no-document

# Copy all of the COSMOS configs in the current working directory into the
#   container at /opt/cosmos
COPY . /opt/cosmos/
WORKDIR /opt/cosmos

# Install COSMOS dependencies
RUN bundle install

# Start script entry point
# CMD bash /opt/cosmos/start.sh
