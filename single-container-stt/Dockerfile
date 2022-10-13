# The catalog is extracted from the generic-models image
FROM cp.icr.io/cp/watson-speech/generic-models@sha256:869ee2a7ca9b6b4c54acf72fb642fda21739716585b577bd73bd4954c88ba3b4 as catalog
FROM cp.icr.io/cp/watson-speech/en-us-multimedia@sha256:1b62ac2a26779febd3077fc404580b0657fb259fc3a25914da105a7c10681bdd AS en-us-multimedia
FROM cp.icr.io/cp/watson-speech/fr-fr-multimedia@sha256:4b4e0dc0748622b964bd39e449020345fb2584f94e93cfa04d7eef5642302147 AS fr-fr-multimedia

FROM cp.icr.io/cp/watson-speech/chuck@sha256:c429d475ba86cbb68b1abe710c0007aad4a3e9103aeff1b328ca908db6d3df12 AS chuck_base

ENV GROUP_KEY=default
ENV CHUCK_VAR=/opt/ibm/chuck.x86_64/var
ENV CLOUD_ENVIRONMENT=icp
ENV LOGHANDLER=KibanaLogHandler
ENV SERVICE_TYPE=speech
ENV COMPONENT=runtime
ENV GROUP=default
ENV TRACK=stable

# Copy in the catalog and runtime configurations
COPY --chown=watson:0 --from=catalog catalog.json ${CHUCK_VAR}/catalog.json
COPY --chown=watson:0 ./chuck_var/* ${CHUCK_VAR}/

FROM chuck_base as model_cache

# Copy model archives from model images
RUN sudo mkdir -p /models/pool2
COPY --chown=watson:0 --from=en-us-multimedia model/* /models/pool2/
COPY --chown=watson:0 --from=fr-fr-multimedia model/* /models/pool2/

# Run script to initialize the model cache from the model archives
COPY ./prepareModels.sh .
RUN ./prepareModels.sh

FROM chuck_base as release

COPY --from=model_cache ${CHUCK_VAR}/cache/ ${CHUCK_VAR}/cache/
