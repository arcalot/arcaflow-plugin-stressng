# Package path for this plugin module relative to the repo root
ARG package=arcaflow_plugin_stressng
ARG stressng_version=stress-ng-0.15.00-1.el8

# STAGE 1 -- Build module dependencies and run tests
# The 'poetry' and 'coverage' modules are installed and verson-controlled in the
# quay.io/arcalot/arcaflow-plugin-baseimage-python-buildbase image to limit drift
FROM quay.io/arcalot/arcaflow-plugin-baseimage-python-buildbase:0.3.1@sha256:9767207e2de6597c4d6bd2345d137ac03661326734d4e6824840d270d3415e12 as build
ARG package
ARG stressng_version
RUN dnf -y install ${stressng_version}


COPY poetry.lock /app/
COPY pyproject.toml /app/

# Convert the dependencies from poetry to a static requirements.txt file
RUN python -m poetry install --without dev --no-root \
 && python -m poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY ${package}/ /app/${package}
COPY tests /app/${package}/tests

ENV PYTHONPATH /app/${package}
WORKDIR /app/${package}

# Run tests and return coverage analysis
# # RUN python -m coverage run tests/test_${package}.py \
# #  && python -m coverage html -d /htmlcov --omit=/usr/local/*


# STAGE 2 -- Build final plugin image
FROM quay.io/arcalot/arcaflow-plugin-baseimage-python-osbase:0.3.1@sha256:0e9384416ad5dd8810c410a87c283ca29a368fc85592378b85261fce5f9ecbeb
ARG package
ARG stressng_version
RUN dnf -y install ${stressng_version}

COPY --from=build /app/requirements.txt /app/
# # COPY --from=build /htmlcov /htmlcov/
COPY LICENSE /app/
COPY README.md /app/
COPY ${package}/ /app/${package}

# Install all plugin dependencies from the generated requirements.txt file
RUN python -m pip install -r requirements.txt

WORKDIR /app/${package}

ENTRYPOINT ["python3", "stressng_plugin.py"]
CMD []

LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugins-stressng"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Arcaflow stress-ng workload plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"
LABEL io.github.arcalot.arcaflow.plugin.privileged="0"
LABEL io.github.arcalot.arcaflow.plugin.hostnetwork="0"
