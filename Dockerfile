FROM docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.11.0

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
