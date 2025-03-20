FROM mambaorg/micromamba:2.0

# install git (for arrakis-server packages)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# install dependencies
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -f /tmp/environment.yml && \
    micromamba clean --all --yes

# install arrakis-server
ARG MAMBA_DOCKERFILE_ACTIVATE=1
COPY --chown=$MAMBA_USER:$MAMBA_USER *.whl /tmp
RUN pip install --no-deps /tmp/*.whl

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "arrakis-server"]
CMD ["--backend", "mock"]
