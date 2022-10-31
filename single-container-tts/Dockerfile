# Model images
FROM cp.icr.io/cp/ai/watson-tts-generic-models:1.0.0 AS catalog
# Add additional models here
FROM cp.icr.io/cp/ai/watson-tts-en-us-michaelv3voice:1.0.0 AS en-us-voice
FROM cp.icr.io/cp/ai/watson-tts-fr-ca-louisev3voice:1.0.0 AS fr-ca-voice

# Base image for the runtime
FROM cp.icr.io/cp/ai/watson-tts-runtime:1.0.0 AS runtime

# Environment variable used for directory where configurations are mounted
ENV CONFIG_DIR=/opt/ibm/chuck.x86_64/var

# Copy in the catalog and runtime configurations
COPY --chown=watson:0 --from=catalog catalog.json ${CONFIG_DIR}/catalog.json
COPY --chown=watson:0 ./config/* ${CONFIG_DIR}/

# Intermediate image to populate the model cache
FROM runtime as model_cache

# Copy model archives from model images
RUN sudo mkdir -p /models/pool2

# For each additional models, copy the line below with the model image
COPY --chown=watson:0 --from=en-us-voice model/* /models/pool2/
COPY --chown=watson:0 --from=fr-ca-voice model/* /models/pool2/

# Run script to initialize the model cache from the model archives
COPY ./prepareModels.sh .

RUN ./prepareModels.sh

# Final runtime image with models baked in
FROM runtime as release

COPY --from=model_cache ${CONFIG_DIR}/cache/ ${CONFIG_DIR}/cache/
