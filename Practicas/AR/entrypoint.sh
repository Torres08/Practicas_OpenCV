#!/bin/bash
groupmod -g $(ls -l /dev/video0 | cut -d\  -f4) video
echo "PATH=$PATH:/home/cuia/.local/bin/" >> /home/cuia/.bashrc
echo 'alias jupyterlab="jupyter-lab --ip=$(hostname -I)"' >> /home/cuia/.bashrc

su -s /bin/bash cuia

