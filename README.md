# adapt_object_mesh

[![Version](https://img.shields.io/docker/v/fnndsc/pl-adapt_object_mesh?sort=semver)](https://hub.docker.com/r/fnndsc/pl-adapt_object_mesh)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-adapt_object_mesh)](https://github.com/FNNDSC/pl-adapt_object_mesh/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-adapt_object_mesh/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-adapt_object_mesh/actions/workflows/ci.yml)

`pl-adapt_object_mesh` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in ...  as input files and
creates ... as output files.

## Abstract

...

## Installation

`pl-adapt_object_mesh` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-adapt_object_mesh)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-adapt_object_mesh` as a container:

```shell
singularity exec docker://fnndsc/pl-adapt_object_mesh adapt_object_mesh_wrapper [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-adapt_object_mesh adapt_object_mesh_wrapper --help
```

## Examples

`adapt_object_mesh_wrapper` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-adapt_object_mesh:latest adapt_object_mesh_wrapper [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-adapt_object_mesh .
```

### Running

Mount the source code `adapt_object_mesh_wrapper.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/adapt_object_mesh_wrapper.py:/usr/local/lib/python3.10/site-packages/adapt_object_mesh_wrapper.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-adapt_object_mesh adapt_object_mesh_wrapper /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-adapt_object_mesh:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-adapt_object_mesh:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-adapt_object_mesh:1.2.3 .
docker push docker.io/fnndsc/pl-adapt_object_mesh:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-adapt_object_mesh:dev chris_plugin_info > chris_plugin_info.json
```

