FROM trevorj/boilerplate:rolling
MAINTAINER Trevor Joynson "<docker@trevor.joynson.io>"

ARG APP_ENV=test

##
## Python base
##

ARG PYTHON=python3

RUN py="${PYTHON%2}" \
 && lazy-apt \
    ${py} \
    ${py}-dev \
    ${py}-pip \
    ${py}-wheel \
    ${py}-virtualenv \
    virtualenv \
 && :

ENV VIRTUAL_ENV="/venv"
ENV PATH="$APP_PATH:$VIRTUAL_ENV/bin:$IMAGE_PATH:$PATH"

RUN set -exv \
 && virtualenv -p "$(which "$PYTHON")" "${VIRTUAL_ENV}" \
 && pip install -U pip setuptools \
 && :

ADD requirements requirements
RUN install-reqs requirements/*

ADD setup.cfg setup.py MANIFEST.in README.* ./

ARG MEINCONF_VERSION=0.0.1dev

ENV PBR_VERSION=$MEINCONF_VERSION

RUN fake-python-package . 'meinconf' \
 && pip install -e .

ADD pytest.ini tox.ini ./
ADD meinconf meinconf
ADD tests tests

CMD ["tox"]

