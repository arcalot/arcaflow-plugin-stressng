FROM quay.io/centos/centos:stream8

RUN dnf module -y install python39 && dnf install -y python39 python39-pip && dnf -y install stress-ng-0.14.00-1.el8

RUN mkdir /stressng
RUN chmod 777 /stressng
ADD stressng_plugin.py /stressng/
ADD poetry.lock /stressng/
ADD pyproject.toml /stressng/
ADD stressng_example.yaml /stressng/
ADD test_stressng_plugin.py /stressng/
RUN chmod +x /stressng/stressng_plugin.py /stressng/test_stressng_plugin.py
ADD https://raw.githubusercontent.com/arcalot/arcaflow-plugins/main/LICENSE /plugin
WORKDIR /stressng

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

USER 1000

ENTRYPOINT ["/stressng/stressng_plugin.py"]
CMD []

LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugins/tree/main/python/stressng"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Arcaflow stress-ng workload plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"
LABEL io.github.arcalot.arcaflow.plugin.privileged="0"
LABEL io.github.arcalot.arcaflow.plugin.hostnetwork="0"
