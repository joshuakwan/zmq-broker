FROM ubuntu:latest

LABEL author=guanjun@cn.ibm.com

EXPOSE 15554
EXPOSE 15555

RUN \
  apt-get update && \
  apt-get install git libtool-bin libtool pkg-config build-essential autoconf automake libzmq-dev net-tools -y && \
  git clone https://github.com/zeromq/libzmq && \
  cd libzmq && ./autogen.sh && ./configure && make -j 4 && \
  make check && make install && ldconfig

RUN \
  apt-get install python python-dev python-pip -y && \
  pip install pyzmq

ADD zmq-broker.py .

ENV FRONTEND_HOST 0.0.0.0
ENV FRONTEND_PORT 15554
ENV BACKEND_HOST 0.0.0.0
ENV BACKEND_PORT 15555

CMD python -u zmq-broker.py $FRONTEND_HOST $FRONTEND_PORT $BACKEND_HOST $BACKEND_PORT
