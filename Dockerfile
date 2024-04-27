FROM alpine:3.19 AS rootfs-stage

ARG S6_OVERLAY_VERSION="3.1.6.2"
ARG TARGETPLATFORM

RUN apk add --no-cache \
    curl \
    bash \
    xz

RUN mkdir /root-out/

# add s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-noarch.tar.xz

RUN case ${TARGETPLATFORM} in \
        "linux/amd64") S6_OVERLAY_ARCH="x86_64" ;; \
        "linux/arm/v7") S6_OVERLAY_ARCH="armhf" ;; \
        "linux/arm64") S6_OVERLAY_ARCH="aarch64" ;; \
        *) S6_OVERLAY_ARCH="x86_64" ;; \
    esac \
    && curl -s -L https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz \
       --output /tmp/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz \
    && tar -C /root-out/ -Jxpf /tmp/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz

# add s6 optional symlinks
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-symlinks-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-symlinks-arch.tar.xz

FROM python:3.11-alpine3.19

WORKDIR /app
COPY --from=rootfs-stage /root-out/ /

ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    PYTHONDONTWRITEBYTECODE=1

RUN \
    echo "**** install runtime packages ****" && \
    apk add --no-cache \
        alpine-release \
        bash \
        ca-certificates \
        coreutils \
        shadow \
        tzdata && \
    echo "**** create abc user and create /data folder ****" && \
    groupmod -g 1000 users && \
    useradd -u 911 -U -d /config -s /bin/false abc && \
    usermod -G users abc && \
    mkdir -p /data \
    echo "**** cleanup ****" && \
    rm -rf \
        /tmp/*

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# copy app and services
COPY tmdb_notifier/ tmdb_notifier/
COPY etc/ /etc/

ENTRYPOINT ["/init"]