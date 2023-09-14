# Run a Single-Container Speech-to-Text Service on Docker

This recipe shows how you can run a single-container Speech-to-Text (STT) service on your local machine using Docker.

## Prerequisites

- Ensure you have your [entitlement key](https://myibm.ibm.com/products-services/containerlibrary) to access the IBM Entitled Registry. [Get a Watson Speech to Text trial license](https://www.ibm.com/account/reg/us-en/subscribe?formid=urx-51754).
- [Docker](https://docs.docker.com/get-docker/) is installed.
- Note that these libraries are only supported on x86 architectures.

**Tip**:

- [Podman](https://podman.io/getting-started/installation) provides a Docker-compatible command line front end. Unless otherwise noted, all the the Docker commands in this tutorial should work for Podman, if you simply alias the Docker CLI with `alias docker=podman` shell command.

## Step 1: Login to the IBM Entitled Registry

IBM Entitled Registry contains various container images for Watson Speech. Once you've obtained the entitlement key for the [container software library](https://myibm.ibm.com/products-services/containerlibrary), you can login to the registry with the key, and pull the container images to your local machine.

```sh
echo $IBM_ENTITLEMENT_KEY | docker login -u cp --password-stdin cp.icr.io
```

## Step 2: Clone the sample code repository

```sh
git clone https://github.com/ibm-ecosystem-engineering/Watson-Speech.git
```

Go to the directory containing the sample code for this tutorial.

```sh
cd Watson-Speech/single-container-stt
```

## Step 3: Build the container image

Build a container image with the provided `Dockerfile`.

```sh
docker build . -t stt-standalone
```

The build process uses configuration files from the `chuck_var` directory. The resulting image will serve two pretrained models ( `en-us-multimedia` and `fr-fr-multimedia` ) supporting two different languages: English (en_US) and French (fr_FR). 

Other [models](https://www.ibm.com/docs/en/watson-libraries?topic=home-models-catalog) can be added to support other languages by updating the provided `Dockerfile`, as well as `env_config.json` and `sessionPools.yaml` in the `chuck_var` directory.

## Step 4: Run the container to start the STT service

You can run the container on Docker, using the container image created in the previous step. The environment variable ACCEPT_LICENSE must be set to true in order for the container to run. To view the set of licenses, run the container without the enviroment variable set.

Run the service in the foreground with the following command.

```sh
docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 stt-standalone
```

## Step 5: Query the STT service

Open up another terminal to query the service. To start, get a of the language models available from the service.

```sh
curl "http://localhost:1080/speech-to-text/api/v1/models"
```

You will see output similar to the following.

```sh
{
   "models": [
      {
         "name": "en-US_Multimedia",
         "rate": 16000,
         "language": "en-US",
         "description": "US English multimedia model for broadband audio (16kHz or more)",
         "supported_features": {
            "custom_acoustic_model": false,
            "custom_language_model": true,
            "low_latency": true,
            "speaker_labels": true
         },
         "url": "http://localhost:1080/speech-to-text/api/v1/models/en-US_Multimedia"
      },
      {
         "name": "fr-FR_Multimedia",
         "rate": 16000,
         "language": "fr-FR",
         "description": "French multimedia model for broadband audio (16kHz or more)",
         "supported_features": {
            "custom_acoustic_model": false,
            "custom_language_model": true,
            "low_latency": true,
            "speaker_labels": true
         },
         "url": "http://localhost:1080/speech-to-text/api/v1/models/fr-FR_Multimedia"
      }
   ]
```

Next, try getting transcriptions from speech samples in the `sample_dataset` directory. For English audio samples, use the default STT model which is configured as `en-US_Multimedia` in `env_config.json`:

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

In both cases, transcriptions (in JSON format) are returned as standard output of the ```curl``` commands.
