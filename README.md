# wolfshark-backend
#OpenDataHack2017 @CopernicusECMPWF challenge #10 (backend)

First, you will need to verify all Python 3 dependencies are installed:

```
pip3 install -r requirements.txt
```

Secondly, make sure you have relatively recent FFMPEG package installed in your
system available via global path.

Finally, you need a PostgreSQL instance either via docker or locally, but
note that the configuration should be as following:

For a postgres instance in a docker container:

```
docker run --name shark -e POSTGRES_PASSWORD=pa55w0rd -d -p 5432:5432 postgres
```

For a local instance setup, name should be `postgres`, user `postgres` and
password `pa55w0rd`.

You will also need to create a file in your root directory (~) called .cdsapirc
containing:

```
url: https://cds.climate.copernicus.eu/api/v2
key: __insert api key here__
```

Finally, to run the server, start it with following command (from inside this
directory):

```
python3 server.py
```
