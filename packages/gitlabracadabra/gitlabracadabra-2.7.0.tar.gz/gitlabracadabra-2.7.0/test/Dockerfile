ARG IMAGE

# DL3006 Always tag the version of an image explicitly
# hadolint ignore=DL3006
FROM $IMAGE

COPY test-requirements.txt /usr/share/gitlabracadabra/

USER root

# SC1091 Not following: File not included in mock
# hadolint ignore=SC1091
RUN . venv/bin/activate && \
  pip install --no-cache-dir -r test-requirements.txt

COPY --chown=1000:1000 tests /usr/share/gitlabracadabra/tests

USER 1000

RUN pytest -p no:cacheprovider
