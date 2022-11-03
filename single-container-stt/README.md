# Run a Single-Container Speech-to-Text Service on Docker

This recipe shows how you can run a single-container Speech-to-Text (STT) service on your local machine using Docker.

## Prerequisites

- Ensure you have your [entitlement key](https://myibm.ibm.com/products-services/containerlibrary) to access the IBM Entitled Registry. [Get a Watson Speech to Text trial license](https://www.ibm.com/account/reg/us-en/subscribe?formid=urx-51754).
- [Docker](https://docs.docker.com/get-docker/) is installed.

**Tip**:

- [Podman](https://podman.io/getting-started/installation) provides a Docker-compatible command line front end. Unless otherwise noted, all the the Docker commands in this tutorial should work for Podman, if you simply alias the Docker CLI with `alias docker=podman` shell command.

## Step 1: Login to the IBM Entitled Registry

IBM Entitled Registry contains various container images for Watson Speech. Once you've obtained the entitlement key for the [container software library](https://myibm.ibm.com/products-services/containerlibrary), you can login to the registry with the key, and pull the container images to your local machine.

```sh
echo $IBM_ENTITLEMENT_KEY | docker login -u cp --password-stdin cp.icr.io
```

## Step 2: Clone the sample code repository

```sh
git clone https://github.com/ibm-build-lab/Watson-Speech.git
```

Go to the directory containing the sample code for this tutorial.

```sh
cd Watson-Speech/single-container-stt
```

## Step 3: Build the container image

Build a container image with the provided `Dockerfile` with two pretrained models ( `en-us-multimedia` and `fr-fr-multimedia` ) included to support two different languages: English (en_US) and French (fr_FR). More [models](https://www.ibm.com/docs/en/watson-libraries?topic=home-models-catalog) can be added to support other languages by updating the provided `Dockerfile`, as well as `env_config.json` and `sessionPools.yaml` in the `chuck_var` directory.

```sh
docker build . -t stt-standalone
```

## Step 4: Run the container to start the STT service

You can run the container on Docker, using the container image created in the previous step. The environment variable ACCEPT_LICENSE must be set to true in order for the container to run. To view the set of licenses, run the container without the enviroment variable set.

Run in the foreground:

```sh
docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 stt-standalone
```

You can also save the licenses to a file:

```sh
docker run --rm -it --publish 1080:1080 stt-standalone > stt-licenses.txt
```

List the language models available:

```sh
curl "http://localhost:1080/speech-to-text/api/v1/models"
```

## Step 5: Query the STT service

Open up another terminal, and query the service with the commands below, which transcribe the audio samples in the `sample_dataset` directory.

For English audio samples, use the default STT model which is configured as `en-US_Multimedia` in `env_config.json`:

```sh
curl "http://localhost:1080/speech-to-text/api/v1/recognize" \
  --header "Content-Type: audio/wav" \
  --data-binary @sample_dataset/en-quote-1.wav
```

For French audio samples, specify the model `fr-FR_Multimedia`:

```sh
curl "http://localhost:1080/speech-to-text/api/v1/recognize?model=fr-FR_Multimedia" \
  --header "Content-Type: audio/wav" \
  --data-binary @sample_dataset/fr-quote-1.wav
```
