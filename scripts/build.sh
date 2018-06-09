#! /bin/sh

apt-get -y update
apt-get -y install wget
apt-get -y install build-essential
apt-get -y install cmake
apt-get -y install python3 python3-pip
apt-get -y install gfortran
apt-get -y install libboost1.65-dev
apt-get -y install proj-bin libproj-dev

apt-get -y libcairo2-dev


pip3 install -r requirements.txt

mkdir -p dependencies/magics
mkdir -p dependencies/eccodes
mkdir -p dependencies/m-build
mkdir -p dependencies/e-build

cd dependencies

wget "https://uc7a02f735c83b9c9fda82c74aa8.dl.dropboxusercontent.com/cd/0/get/AIcLaMgEqPZNa7Sa4fJk9IriRukU7KHrg5WreNXbIjk8vl3KkPjVugkTSEg9KJeAM6bvsJ7b-jZqGt32NMqfwSqzCSAQ2rATMIVgdpY4ffJBHy_oL1sF1fU7OH3FIcT_1GCyURFjHe4s1VLZUCYf90TWx4_iwePtzVzl8xXp60AydLhiZgZ3FSWTglNa3prVjIU/file?_download_id=7103605597495736221321059534091427937461954770407019847160071680414&_notify_domain=www.dropbox.com&dl=1" -O magics-source.tgz

tar -xzvf magics-source.tgz
rm magics-source.tgz

MAGICS_SOURCE='Magics-3.1.0-Source'

wget https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-2.7.3-Source.tar.gz?api=v2 -O eccodes-2.7.3-Source.tgz

tar -xzvf eccodes-2.7.3-Source.tgz

ECCODES_SOURCE='eccodes-2.7.3-Source'

cd e-build
cmake "../$ECCODES_SOURCE"
make -j4
make install

cd ..

cd m-build
cmake -DENABLE_CAIRO=OFF -DENABLE_ODB=OFF "../$MAGICS_SOURCE"
make -j4 
make install

cd ../../


