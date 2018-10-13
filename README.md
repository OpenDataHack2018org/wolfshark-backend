# WolfShark (backend)

> #OpenDataHack2017 @CopernicusECMPWF challenge #10
> Automated visualization and animation generator based on climate data.

## Setup

First, you will need to verify all Python 3 dependencies are installed:

```
pip3 install -r docker/requirements.txt
```

Secondly, make sure you have relatively recent FFMPEG package installed in your
system available via global path.

Finally, you need a PostgreSQL instance either via docker or locally, but
note that the configuration should be as following:

* database name: `docker`
* user name: `docker`
* password: `pa55w0rd`

You will also need to create a file in your root directory (~) called .cdsapirc
containing:

```
url: https://cds.climate.copernicus.eu/api/v2
key: <UID>:<KEY>
```

where <UID> is your Copernicus Climate Data Store User ID, and <KEY> is your API
Key, you can find them both in your profile.

Finally, to run the server, start it with following command (from inside this
directory):

```
python3 server.py
```

The app will be visible under http://localhost:5000 by default.

## Docker Support

Alternatively, you can use the docker image, please start it with following command:

```
docker run --name wolfshark -d -p 5000:5000 -e API_KEY=<UID>:<KEY> dvuckovic/wolfshark:latest
```

In order to build the docker image locally and use it instead, try the following:

```
cd docker
docker build -t wolfshark .
docker run --name wolfshark -d -p 5000:5000 -e API_KEY=<UID>:<KEY> wolfshark
```
