#!/usr/bin/env bash

if [ ! -z $API_KEY ]
then
    echo "url: https://cds.climate.copernicus.eu/api/v2" > /root/.cdsapirc
    echo "key: $API_KEY" >> /root/.cdsapirc
fi

if [ ! -e /root/.cdsapirc ]
then
    echo "Please define API_KEY environment variable before running the container again, i.e.:"
    echo
    echo "    docker run --name wolfshark -p 5000:5000 -e API_KEY=<UID>:<KEY> wolfshark"
    echo
    echo "where <UID> is your Copernicus Climate Data Store User ID, and <KEY> is your API Key, you can find them both in your profile."
    echo
    exit 1
fi
