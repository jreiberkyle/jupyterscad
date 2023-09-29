#!/bin/bash
# run this from the notebook root directory
podman run -it --rm -p 8888:8888 -v "$(pwd)":/app jupyterscad
