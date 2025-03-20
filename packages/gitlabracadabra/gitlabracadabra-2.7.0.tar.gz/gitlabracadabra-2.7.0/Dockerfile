# stage builder
FROM python:3.13.2-slim@sha256:f3614d98f38b0525d670f287b0474385952e28eb43016655dd003d0e28cf8652 as builder

WORKDIR /usr/share/gitlabracadabra

# DL3013 Pin versions in pip
# hadolint ignore=DL3013
RUN pip install --no-cache-dir build

COPY . .

RUN python -m build

# =================================================================
# stage venv
FROM python:3.13.2-slim@sha256:f3614d98f38b0525d670f287b0474385952e28eb43016655dd003d0e28cf8652 as venv

WORKDIR /usr/share/gitlabracadabra

RUN python -m venv /usr/share/gitlabracadabra/venv

COPY requirements.txt .

# SC1091 Not following: File not included in mock
# hadolint ignore=SC1091
RUN . venv/bin/activate && \
  pip install --no-cache-dir -r requirements.txt

COPY --from=builder /usr/share/gitlabracadabra/dist/gitlabracadabra-*-py3-none-any.whl .

# SC1091 Not following: File not included in mock
# hadolint ignore=SC1091
RUN . venv/bin/activate && \
  pip install --no-cache-dir ./gitlabracadabra-*-py3-none-any.whl

# =================================================================
# stage run
FROM python:3.13.2-slim@sha256:f3614d98f38b0525d670f287b0474385952e28eb43016655dd003d0e28cf8652

WORKDIR /usr/share/gitlabracadabra

COPY --from=venv /usr/share/gitlabracadabra/venv ./venv

# DL3008 Pin versions in apt get install
# hadolint ignore=DL3008
RUN --mount=type=cache,from=builder,source=/usr/share/gitlabracadabra/urllib3-Lower-retry-message-from-WARNING-to-INFO.patch,target=/tmp/urllib3-Lower-retry-message-from-WARNING-to-INFO.patch \
  set -x && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  ca-certificates \
  patch \
  && \
  rm -rf /var/lib/apt/lists/* && \
  patch venv/lib/python*/site-packages/urllib3/connectionpool.py < /tmp/urllib3-Lower-retry-message-from-WARNING-to-INFO.patch && \
  apt-get purge -y patch && \
  adduser --disabled-password --gecos '' gitlabracadabra

ENTRYPOINT ["gitlabracadabra"]
ENV PATH="/usr/share/gitlabracadabra/venv/bin:$PATH"
USER 1000
LABEL org.opencontainers.image.source="https://gitlab.com/gitlabracadabra/gitlabracadabra"
