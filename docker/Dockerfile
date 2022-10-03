FROM ubuntu:22.04

ENV TZ Europe/Paris

LABEL maintainer="Erwin Lejeune <erwin.lejeune15@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get install -y --no-install-recommends wget && \
    apt-get install -y --no-install-recommends git && \
    apt-get install -y --no-install-recommends python3-pytest && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    apt-get install -y --no-install-recommends python3-dotenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN git clone  https://github.com/guilyx/python-nexo.git

WORKDIR /python-nexo

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY docker/entrypoint.sh /.

RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT [ "/entrypoint.sh" ]