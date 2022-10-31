# Deploy a Text-to-Speech Service with Docker
This tutorial demonstrates how you can deploy a single-container Text-to-Speech (TTS) service on your local machine using Docker. 

## Prerequisites
- Ensure you have your [entitlement key](https://myibm.ibm.com/products-services/containerlibrary) to access the IBM Entitled Registry
- [Docker](https://docs.docker.com/get-docker/) is installed

**Tip**:
- [Podman](https://podman.io/getting-started/installation) provides a Docker-compatible command line front end. Unless otherwise noted, all the the Docker commands in this tutorial should work for Podman, if you simply alias the Docker CLI with `alias docker=podman` shell command.


## Steps

## Step 1: Login to the IBM Entitled Registry
IBM Entitled Registry contains various container images for Watson Speech. Once you've obtained the entitlement key from the [container software library](https://myibm.ibm.com/products-services/containerlibrary), you can login to the registry with the key, and pull the container images to your local machine.
```
echo $IBM_ENTITLEMENT_KEY | docker login -u cp --password-stdin cp.icr.io
```

### Step 2. Checkout the sample code
```
git clone git@github.com:ibm-build-lab/Watson-Speech.git
```
Go to the directory for this tutorial.
```
cd Watson-Speech/single-container-tts
```

### Step 3. Build the container image
Build a container image with the provided `Dockerfile`. The containers serve two pretrained models: `en-us-michaelv3voice` (US English) and `fr-ca-louisev3voice` (Candian French). Additional models can be added to support other languages by updating the provided `Dockerfile`, as well as `env_config.json` and `sessionPools.yaml` in the `config` directory.
```
docker build . -t tts-standalone
```

### Step 4. Run the service
You can run the container on Docker as follows, using the container image created in the previous step. 
```
docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone
```
This runs the service in the foreground.

### Step 5. Test the service
Open up another terminal. First, query the models that are available from the service.
```
curl "http://localhost:1080/text-to-speech/api/v1/voices"
```
You will see output similar to the following.
```

   "voices": [
      {
         "name": "en-US_MichaelV3Voice",
         "language": "en-US",
         "gender": "male",
         "description": "Michael: American English male voice. Dnn technology.",
         "customizable": true,
         "supported_features": {
            "custom_pronunciation": true,
            "voice_transformation": false
         },
         "url": "http://localhost:1080/text-to-speech/api/v1/voices/en-US_MichaelV3Voice"
      },
      {
         "name": "fr-CA_LouiseV3Voice",
         "language": "fr-CA",
         "gender": "female",
         "description": "Louise: French Canadian female voice. Dnn technology.",
         "customizable": true,
         "supported_features": {
            "custom_pronunciation": true,
            "voice_transformation": false
         },
         "url": "http://localhost:1080/text-to-speech/api/v1/voices/fr-CA_LouiseV3Voice"
      }
   ]
```
Generate an audio file in English. 
```
curl "http://localhost:1080/text-to-speech/api/v1/synthesize" \
  --header "Content-Type: application/json" \
  --data '{"text":"Hello world"}' \
  --header "Accept: audio/wav" \
  --output output.wav
```
The audio will be in `output.wav`. Next, try French.
```
curl "http://localhost:1080/text-to-speech/api/v1/synthesize?voice=fr-CA_LouiseV3Voice" \
  --header "Content-Type: application/json" \
  --data '{"text":"Bonjour le monde."}' \
  --header "Accept: audio/wav" \
  --output french-test.wav
```
The output audio will be in `french-test.wav`.
