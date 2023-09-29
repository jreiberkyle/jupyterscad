#!/bin/bash

podman machine init --cpus=4 --disk-size=10 --memory=6096 -v $HOME:$HOME
