# wolfshark-backend
#OpenDataHack2017 @CopernicusECMPWF challenge #10 (backend)

To install you will need to pip install the following:

* peewee
* psycopg2-binary
* flask
* flask-restful

* a postgres instance either docker or local but the details have to be as following\

run with docker command below and 0.0.0.0 as the host in job.py and server.py

```
 docker run --name shark -e POSTGRES_PASSWORD=pa55w0rd -d -p 5432:5432 postgres
```

or a local instance with name postgres, user postgres and password pa55w0rd