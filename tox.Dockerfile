# FROM themattrix/tox-base

FROM geometalab/gdal-docker:v3.0.0

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.UTF-8

ENV PYENV_ROOT="/.pyenv" \
    PATH="/.pyenv/bin:/.pyenv/shims:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates curl && \
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash && \
    apt-get purge -y --auto-remove ca-certificates curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
        libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
        libxml2-dev libxmlsec1-dev libffi-dev \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pyenv update && \
            pyenv install 3.7.3 && \
            pyenv global $(pyenv versions --bare) && \
            find $PYENV_ROOT/versions -type d '(' -name '__pycache__' -o -name 'test' -o -name 'tests' ')' -exec rm -rfv '{}' + && \
            find $PYENV_ROOT/versions -type f '(' -name '*.py[co]' -o -name '*.exe' ')' -exec rm -fv '{}' +

RUN pyenv local 3.7.3 && \
    python -m pip install -U pip && \
    python -m pip install tox && \
    pyenv local --unset && \
    pyenv rehash

COPY . /app/
WORKDIR /app/

CMD tox
