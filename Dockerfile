# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.11.0-slim-bullseye

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="adapt_object_mesh" \
      org.opencontainers.image.description="A ChRIS plugin wrapper around adapt_object_mesh from MINC tools"

WORKDIR /usr/local/src/pl-adapt_object_mesh

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["adapt_object_mesh_wrapper", "--help"]
