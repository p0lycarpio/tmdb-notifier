FROM alpine:3.18 AS rootfs-stage

ARG S6_OVERLAY_VERSION="3.1.6.0"

ARG TARGETPLATFORM
RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then S6_OVERLAY_ARCH=amd64; \
    elif [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then S6_OVERLAY_ARCH=arm; \
    elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then S6_OVERLAY_ARCH=aarch64; \
    else S6_OVERLAY_ARCH=amd64; fi

RUN apk add --no-cache \
    bash \
    xz

RUN mkdir /root-out/

# add s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz

# add s6 optional symlinks
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-symlinks-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz /tmp
RUN tar -C /root-out/ -Jxpf /tmp/s6-overlay-symlinks-arch.tar.xz

FROM python:3.10-alpine3.18

WORKDIR /app
COPY --from=rootfs-stage /root-out/ /

ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    PYTHONDONTWRITEBYTECODE=1

# install packages
RUN apk add --no-cache \
    alpine-release \
    bash \
    ca-certificates \
    coreutils \
    redis=7.0.15-r0 \
    tzdata && \
    rm -rf /tmp/*

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# copy app and services
COPY src/ /app/
COPY etc/ /etc/

ENTRYPOINT ["/init"]