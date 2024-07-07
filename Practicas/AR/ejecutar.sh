#!/bin/bash
/usr/bin/xhost +local:*
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v ./:/host/ --privileged --expose 8888 --user root --gpus=all --rm --name=cuia -it cuia
