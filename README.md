# wolfshark-backend
#OpenDataHack2017 @CopernicusECMPWF challenge #10 (backend)

To install you will need to verify all dependencies are installed:

```
pip3 install -r requirements.txt
```

Additionally, you need a PostgreSQL instance either via docker or locally, but
note that the configuration should be as following:

```
docker run --name shark -e POSTGRES_PASSWORD=pa55w0rd -d -p 5432:5432 postgres
```

For a local instance setup, name should be `postgres`, user `postgres` and
password `pa55w0rd`.

Finally, to run the server, start it with following command:

```
python3 server.py
```
