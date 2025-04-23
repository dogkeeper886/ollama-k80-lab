FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Taipei

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip git \
    && pip3 install mcp playwright \
    && playwright install-deps \
    && playwright install

WORKDIR /usr/local/src
RUN git clone https://github.com/random-robbie/mcp-web-browser

CMD [ "/usr/bin/python3", "/usr/local/src/mcp-web-browser/src/mcp_web_browser/server.py" ]