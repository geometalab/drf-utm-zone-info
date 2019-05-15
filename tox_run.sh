#!/bin/bash
set -ex

docker pull geometalab/postgis-with-translit
docker run -d -e POSTGRES_DB='postgres' --name pg_translit_test_db geometalab/postgis-with-translit

docker build -t tox -f tox.Dockerfile .
{ # your 'try' block
    docker run --rm --link="pg_translit_test_db:database" tox
} || { # your 'catch' block
    echo 'failed'
}

docker rm -vf pg_translit_test_db
