# Deploy a Text-to-Speech Service with Docker

## Prerequisites

## Steps

### 1. Checkout the sample code
Clone the sample code used in the speech tutorials.
```
git clone git@github.com:ibm-build-lab/Watson-Speech.git
```
Go to the directory for this tutoraial.
```
cd Watson-Speech/single-container-tts
```

### 2. Build and run
There is a Dockerfile in the directory used to build a container image for the text-to-speech service. Run the following command to build the image.
```
docker build . -t tts-standalone
```
```
docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone
```

### 3. Test the service

```
curl "http://localhost:1080/text-to-speech/api/v1/voices"
```
```
curl "http://localhost:1080/text-to-speech/api/v1/synthesize" \
  --header "Content-Type: application/json" \
  --data '{"text":"Hello world"}' \
  --header "Accept: audio/wav" \
  --output output.wav
```
