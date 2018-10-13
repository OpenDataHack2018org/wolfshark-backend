#
# Build image.
#

FROM debian:stable-slim as build

# Use a reliable Debian mirror (https://github.com/rgeissert/http-redirector/issues/75)
RUN set -ex \
    && sed --in-place 's/httpredir.debian.org/ftp.uk.debian.org/' /etc/apt/sources.list

# Ensure ECMWF's HTTP proxy does not get in the way (thanks to bentorey.hernandez@ecmwf.int).
RUN set -ex \
    && echo 'Acquire::http::Pipeline-Depth "0";' > /etc/apt/apt.conf.d/99fixbadproxy \
    && echo 'Acquire::http::No-Cache=True;' >> /etc/apt/apt.conf.d/99fixbadproxy \
    && echo 'Acquire::BrokenProxy=true;' >> /etc/apt/apt.conf.d/99fixbadproxy

RUN set -ex \
    && apt-get update

# Install build tools.
RUN set -ex \
    && apt-get install --yes --no-install-suggests --no-install-recommends \
      bison \
      bzip2 \
      ca-certificates \
      cmake \
      curl \
      file \
      flex \
      g++-6 \
      gcc-6 \
      gfortran-6 \
      git \
      make \
      patch \
      sudo \
      swig \
      xz-utils

RUN set -ex \
    && ln -s /usr/bin/g++-6 /usr/bin/g++ \
    && ln -s /usr/bin/gcc-6 /usr/bin/gcc

# Install build-time dependencies.
RUN set -ex \
    && apt-get update \
    && apt-get install --yes --no-install-suggests --no-install-recommends \
      libarmadillo-dev \
      libatlas-dev \
      libboost-dev \
      libbz2-dev \
      libc6-dev \
      libcairo2-dev \
      libcurl4-openssl-dev \
      libeigen3-dev \
      libexpat1-dev \
      libfreetype6-dev \
      libfribidi-dev \
      libgdal-dev \
      libgeos-dev \
      libharfbuzz-dev \
      libhdf5-dev \
      libjpeg-dev \
      liblapack-dev \
      libncurses5-dev \
      libnetcdf-dev \
      libpango1.0-dev \
      libpcre3-dev \
      libpng-dev \
      libproj-dev \
      libreadline6-dev \
      libsqlite3-dev \
      libssl-dev \
      libxml-parser-perl \
      libxml2-dev \
      libxslt1-dev \
      libyaml-dev \
      zlib1g-dev \
      gnupg2

# Install Python
ENV PYTHON_VERSION=3.6.5

RUN set -ex \
    && mkdir /src \
    && cd /src \
    && curl --silent https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz | \
       tar xJf -

RUN set -ex \
    && mkdir /build \
    && cd /build \
    && /src/Python-${PYTHON_VERSION}/configure \
       --enable-shared \
    && make -j4 \
    && make install \
    && /sbin/ldconfig

RUN set -x \
    && ln -s /usr/local/bin/pip3 /usr/local/bin/pip \
    && ln -s /usr/local/bin/pydoc3 /usr/local/bin/pydoc \
    && ln -s /usr/local/bin/python3 /usr/local/bin/python \
    && ln -s /usr/local/bin/python3-config /usr/local/bin/python-config

# Ensure local Python is preferred over distribution Python.
ENV PATH=/usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG=C.UTF-8

# Install Python run-time dependencies.
COPY requirements.txt /root/

RUN set -ex \
    && pip install -r /root/requirements.txt

# Install testing support.
# COPY requirements-testing.txt /root/

# RUN set -ex \
#     && pip install -r /root/requirements-testing.txt

# Install application source code.
RUN set -eux \
    && mkdir /code \
    && cd /code \
    && git clone https://github.com/OpenDataHack2018org/wolfshark.git \
    && cd wolfshark \
    && git submodule init \
    && git submodule update

# Install eccodes.
ENV ECCODES_VERSION=eccodes-2.8.0

RUN set -eux \
    && cd /src \
    && mkdir eccodes \
    && cd eccodes \
    && curl -O https://confluence.ecmwf.int/download/attachments/45757960/${ECCODES_VERSION}-Source.tar.gz\?api\=v2 \
    && mv ${ECCODES_VERSION}-Source.tar.gz\?api\=v2 ${ECCODES_VERSION}-Source.tar.gz \
    && tar -xzf ${ECCODES_VERSION}-Source.tar.gz \
    && mkdir /build/eccodes \
    && cd /build/eccodes \
    && cmake /src/eccodes/${ECCODES_VERSION}-Source \
       -DCMAKE_BUILD_TYPE=Release \
       -DENABLE_PYTHON=OFF \
    && make -j4 \
    && make install \
    && /sbin/ldconfig

# Install Magics++.
ENV MAGICS_VERSION=Magics-3.1.0

RUN set -eux \
    && cd /src \
    && mkdir magics \
    && cd magics \
    && curl -O https://confluence.ecmwf.int/download/attachments/3473464/${MAGICS_VERSION}-Source.tar.gz\?api\=v2 \
    && mv ${MAGICS_VERSION}-Source.tar.gz\?api\=v2 ${MAGICS_VERSION}-Source.tar.gz \
    && tar xzvf ${MAGICS_VERSION}-Source.tar.gz \
    && mkdir /build/magics \
    && cd /build/magics \
    && cmake /src/magics/${MAGICS_VERSION}-Source \
       -DCMAKE_BUILD_TYPE=Release \
       -DENABLE_BUFR=OFF \
       -DENABLE_CAIRO=ON \
       -DENABLE_ODB=OFF \
       -DENABLE_PYTHON=ON \
       -DENABLE_FORTRAN=OFF \
    && make -j4 \
    && make install \
    && /sbin/ldconfig

# Remove unneeded files.
RUN set -ex \
    && find /usr/local -name 'lib*.so' | xargs -r -- strip --strip-unneeded || true \
    && find /usr/local/bin | xargs -r -- strip --strip-all || true \
    && find /usr/local/lib -name __pycache__ | xargs -r -- rm -rf




#
# Run-time image.
#

FROM debian:stable-slim

RUN set -ex \
    && groupadd -r wms \
    && useradd -r -g wms -d /home/wms -m wms

# Use a reliable Debian mirror (https://github.com/rgeissert/http-redirector/issues/75)
RUN set -ex \
    && sed --in-place 's/httpredir.debian.org/ftp.uk.debian.org/' /etc/apt/sources.list

# Ensure ECMWF's HTTP proxy does not get in the way (thanks to bentorey.hernandez@ecmwf.int).
RUN set -ex \
    && echo 'Acquire::http::Pipeline-Depth "0";' > /etc/apt/apt.conf.d/99fixbadproxy \
    && echo 'Acquire::http::No-Cache=True;' >> /etc/apt/apt.conf.d/99fixbadproxy \
    && echo 'Acquire::BrokenProxy=true;' >> /etc/apt/apt.conf.d/99fixbadproxy

# Install run-time depencencies.
RUN set -ex \
    && apt-get update \
    && mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get install --yes --no-install-suggests --no-install-recommends \
       ca-certificates \
       curl \
       ghostscript \
       imagemagick \
       ksh \
       libarmadillo7 \
       libbz2-1.0 \
       libcairo-gobject2 \
       libcairo-script-interpreter2 \
       libcairo2 \
       libcroco3 \
       libcurl3 \
       libexif12 \
       libexpat1 \
       libfontconfig1 \
       libfreetype6 \
       libfribidi0 \
       libgdal20 \
       libgeoip1 \
       libgeos-c1v5 \
       libgif7 \
       libgomp1 \
       libgssrpc4 \
       libharfbuzz0b \
       libhdf5-100 \
       libicu57	   \
       libilmbase12 \
       libjbig0 \
       libjpeg62-turbo \
       libjs-jquery \
       liblcms2-2 \
       liblqr-1-0 \
       libncurses5 \
       libnetcdf11 \
       libopenexr22 \
       libpangocairo-1.0-0 \
       libpangoxft-1.0-0 \
       libpcre3 \
       libpcrecpp0v5 \
       libpng16-16 \
       libproj12 \
       libreadline7 \
       libsqlite3-0 \
       libssl1.1 \
       libtiff5 \
       libtiffxx5 \
       libwebp6 \
       libxft2 \
       libxml2 \
       libxslt1.1 \
       poppler-utils \
       rsync \
       zlib1g \
       gnupg2 \
       dirmngr \
       postgresql-client-9.6 \
       postgresql-9.6 \
       postgresql \
       ffmpeg

# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# update the repository sources list
# and install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

# nvm location
RUN mkdir -p /usr/local/nvm

# nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 8.12.0

# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Copy Python run-time and ECMWF software.
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY --from=build /usr/local/lib/ /usr/local/lib/
COPY --from=build /usr/local/share/eccodes/ /usr/local/share/eccodes/
COPY --from=build /usr/local/share/magics/ /usr/local/share/magics/
COPY --from=build /code /code

# Ensure shared libs installed by the previous step are available.
RUN set -ex \
    && /sbin/ldconfig

# Ensure local Python is preferred over distribution Python.
ENV PATH=/usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG=C.UTF-8

# Configure Python runtime.
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER  postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'pa55w0rd';" &&\
    createdb -O docker docker

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.6/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.6/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.6/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER root

# XXX: Important, make sure to leave it to the backend folder, since our server code expects this path.
WORKDIR /code/wolfshark/backend

# Install NPM dependencies and build the production frontend app.
RUN npm install --no-save
RUN npm run build

# Copy API setup script and make it executable.
COPY setup_api_key.sh /root/
RUN chmod +x /root/setup_api_key.sh

# Expose the Flask application port.
EXPOSE 5000

# Setup the API key, and if successful, run PostgreSQL server and Flask application when the container launches.
CMD /root/setup_api_key.sh && /etc/init.d/postgresql start && python server.py
