FROM trevorj/boilerplate:rolling
MAINTAINER Trevor Joynson "<docker@trevor.joynson.io>"

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

ADD setup.py MANIFEST.in README.md pytest.ini setup.cfg setup.py tox.ini ./
ADD meinconf meinconf
ADD tests tests

CMD ["tox"]

