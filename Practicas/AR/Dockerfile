FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 as base

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Madrid

RUN apt-get autoclean
RUN apt-get update --allow-unauthenticated && apt-get -y upgrade
RUN apt-get -y install --no-install-recommends cmake nano gcc g++ python3 python3-numpy python3-dev git python3-setuptools unzip libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgtk-3-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev libopenblas-dev liblapack-dev libavdevice-dev libavfilter-dev libavformat-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev libtesseract-dev tesseract-ocr tesseract-ocr-spa libvtk9-dev libgtkglext1-dev ant libdc1394-dev liblapacke-dev gstreamer1.0-vaapi libvdpau-va-gl1 libffmpeg-nvenc-dev libnvidia-encode-530 libva-dev vainfo libgflags-dev protobuf-compiler libprotobuf-dev libgoogle-glog-dev libceres-dev libogre-1.12-dev libopenjp2-tools libopenjpip-dec-server libopenjpip-server libqt6core5compat6-dev libqt6opengl6-dev

RUN git clone https://github.com/opencv/opencv.git && git clone https://github.com/opencv/opencv_contrib.git && git clone https://github.com/opencv/opencv_extra.git

ENV VIDEOSDK_VERSION 12.1.14
WORKDIR /opt/nvidia/video-sdk
COPY Video_Codec_SDK_${VIDEOSDK_VERSION}.zip /opt/nvidia/video-sdk

RUN unzip -j Video_Codec_SDK_${VIDEOSDK_VERSION}.zip \
          Video_Codec_SDK_${VIDEOSDK_VERSION}/Interface/cuviddec.h \
          Video_Codec_SDK_${VIDEOSDK_VERSION}/Interface/nvcuvid.h \
          Video_Codec_SDK_${VIDEOSDK_VERSION}/Interface/nvEncodeAPI.h \
          -d /usr/local/cuda/include && unzip -j Video_Codec_SDK_${VIDEOSDK_VERSION}.zip \
          Video_Codec_SDK_${VIDEOSDK_VERSION}/Lib/linux/stubs/x86_64/libnvcuvid.so \
          Video_Codec_SDK_${VIDEOSDK_VERSION}/Lib/linux/stubs/x86_64/libnvidia-encode.so \
          -d /usr/local/cuda/lib64/stubs


RUN mkdir /opencv/build
WORKDIR /opencv/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=ON -D WITH_CUDNN=ON -D WITH_CUBLAS=ON -D WITH_TBB=ON -D OPENCV_DNN_CUDA=ON -D OPENCV_ENABLE_NONFREE=ON -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules -D BUILD_EXAMPLES=OFF -D WITH_GTK=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D HAVE_opencv_python3=ON -D Tesseract_LIBRARY="/usr/lib/x86_64-linux-gnu/libtesseract.so" -DTesseract_INCLUDE_DIR="/usr/include/tesseract" -D WITH_TESSERACT=ON -D BUILD_opencv_world=OFF -D VA_INCLUDE_DIR="/usr/local/cuda/include" -D OpenBLAS_INCLUDE_DIR="/usr/include/x86_64-linux-gnu/" -D OpenBLAS_LIB="/usr/lib/x86_64-linux-gnu/" -D LAPACK_LIBRARIES="/usr/lib/x86_64-linux-gnu/lapack/liblapack.so" -D LAPACKE_INCLUDE_DIR="/usr/include/x86_64-linux-gnu" -D LAPACK_INCLUDE_DIR="/usr/include/x86_64-linux-gnu" -D WITH_OPENCL=OFF -D GLOG_INCLUDE_DIR="/usr/include" -DBUILD_opencv_rgbd=OFF ..
RUN make -j$((`nproc`-1)) install

ENV OPENCV_TEST_DATA_PATH=/opencv_extra/testdata/

RUN ln -s /usr/bin/python3 /usr/bin/python


RUN useradd -m -p ubicomp cuia && usermod -aG video cuia

WORKDIR /host
EXPOSE 8888

RUN apt-get -y install --no-install-recommends python3-pip

USER cuia

ENV XDG_RUNTIME_DIR /tmp/runtime-cuia

RUN python3 -m pip install --upgrade pip && pip install jupyterlab matplotlib requests pyside2 nodejs

USER root
RUN apt-get autoclean && apt-get autoremove && rm -r /opencv && rm -r /opencv_contrib
RUN echo 'root:Weiser!' | chpasswd
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
