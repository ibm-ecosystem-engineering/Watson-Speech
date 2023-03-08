# Install IBM Watson Speech to Text Library in OpenShift

IBM Watson® Speech to Text Library (STT) for Embed enables fast and accurate speech transcription to text from spoken audio in multiple languages for a variety of use cases. The service leverages machine learning to combine knowledge of grammar, language structure, and the composition of audio and voice signals to accurately transcribe the human voice.

In this tutorial I am going to show, how to install IBM Watson Speech to Text Embed with runtime and customization in OpenShift. We are going to use the helm chart provided in [here](https://github.com/IBM/ibm-watson-embed-charts/tree/main/charts/ibm-watson-stt-embed) 

## Prerequisites

- [helm 3](https://helm.sh/docs/intro/install/)
- Ensure you have your [entitlement key](https://myibm.ibm.com/products-services/containerlibrary) to access to [the images with an IBM entitlement key](https://www.ibm.com/docs/en/watson-libraries?topic=i-accessing-files)
  - Set entitlemet key in an environment variable
    ```sh
    export IBM_ENTITLEMENT_KEY=<Set the entitlement key>
    ``` 
- For customization
  - S3 Compatible Storage 
  - PostgreSQL Database
- Kubernetes Cluster - the Speech to Text service is assumed to be running in a Kubernetes cluster.

## S3 Compatible Storage

For customization, an S3 compatible storage service must exist that supports HMAC (access key and secret key) credentials. Watson Speech requires one bucket that it can read and write objects to. The bucket will be populated with stock models at install time and will also store customization artifacts, including training data and trained models.

Here are the steps to obtain IBM Cloud S3 bucket HMAC credentials and endpoint. You may choose bucket based on the cloud providers. 

1. Log in to [IBM Cloud](https://cloud.ibm.com/login).
2. From the IBM Cloud Dashboard, click the Cloud Object Storage service instance that you want to work with.
3. To view the endpoint URLs, click Endpoint in the left pane and select your preferred location or region.
4. To view the endpoint URLs, click Endpoint in the left pane and select your preferred location or region.
   1. Copy your preferred public `endpoint` (for example, s3.us.cloud-object-storage.appdomain.cloud) and use it as the value for the `Endpoint URL` field (or `endpointUrl` parameter).
   2. Copy your preferred location or `region` (for example, ap-geo) and use it as the value for the Region field (or region parameter).
5. To view the service credentials, click Service credentials in the left pane, and then click View credentials. (If you want to define new credentials, click New credential, click Advanced options, then select Include HMAC Credential.)
6. Copy the `cos_hmac_keys/secret_access_key` value and use it as the value for the `Secret access key` field (or `secretAccessKey parameter`).
7. Copy the `cos_hmac_keys/access_key_id` value and use it as the value for the `Access key ID` field (or `accessKeyId parameter`).

Set all S3 crededentials and information in environment variable so that we can make use them during stt library installation. Please modify the below script based on the information you collected from the previous steps.

```sh
export S3_BUCKET_NAME=<Endpoint URL>
export S3_ACCESS_KEY=<accessKeyId>
export S3_SECRET_KEY=<secretAccessKey>
export S3_REGION=<Region>
export S3_ENPOINT_URL=<Endpoint URL>
```

example Connecting by using HMAC authentication 

```yaml
  ibmcoss3:
    - name: Account 1
      credentials:
        secretAccessKey: 12a3bcd4567890ef123g4567890hij12k1m3n4567o8901p2
        accessKeyId: 1a2dfbc3d45678901ef2g3h45678i90jkl
        region: ap-geo
      endpoint:
        endpointUrl: s3.us.cloud-object-storage.appdomain.cloud
```

## Install Postgresql

PostgreSQL Database is required to manage metadata related to customization. The customization container uses TLS to Postgres, but always sets up the connection with a "NonValidatingFactory" which does not do cert validation. Here I am going to use a self signed certificate to enable TLS in postgresql database.

Create Certificate authority certificate and key

```sh
openssl req \                                                
  -x509 \
  -nodes \   
  -newkey ec \
  -pkeyopt ec_paramgen_curve:prime256v1 \
  -pkeyopt ec_param_enc:named_curve \
  -sha384 \
  -keyout ca.key \    
  -out ca.crt \    
  -days 3650 \
  -subj "/CN=*"
```

Create certificate signing requrest

```sh
  openssl req \                                                
  -new \ 
  -newkey ec \
  -nodes \
  -pkeyopt ec_paramgen_curve:prime256v1 \
  -pkeyopt ec_param_enc:named_curve \
  -sha384 \
  -keyout server.key \
  -out server.csr \
  -days 365 \ 
  -subj "/CN=postgresql-release-hl"
```

create `server.crt` certificate and key using server key and 

```sh
  openssl x509 \                                               
  -req \ 
  -in server.csr \
  -days 365 \
  -CA ca.crt \                           
  -CAkey ca.key \                    
  -CAcreateserial \
  -sha384 \           
  -out server.crt
```

Create secret for the certifiate you created

```sh
oc create secret tls pg-tls-secret \                      
--cert=server.crt \       
--key=server.key
```
We are using bitnami postgresql packaged in helm charts.

Add bitnami helm chart repo

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Install postgresql helm chart

```sh
helm install postgresql-release bitnami/postgresql \
--set tls.enabled="true" \
--set tls.certificatesSecret="pg-tls-secret" \
--set tls.certFilename="tls.crt" \
--set tls.certKeyFilename="tls.key"
```

In OpenShift cluster Statefulset pod might not spin up because, it needs a extra previllege to run the container.

create service account and assign `anyuid` SCC

```sh
oc create serviceaccount db-sa
oc adm policy add-scc-to-user anyuid -z db-sa
```

Set the service account

```sh
oc set serviceaccount statefulset postgresql-release db-sa
```

Set the Postgresql password in an environment variable for future use

```sh
export POSTGRES_PASSWORD=$(oc get secret --namespace stt-test postgresql-release -o jsonpath="{.data.postgres-password}" | base64 -d)
```
## Install Speech to Text Library embed helm chart

Let start with cloning the helm chart github repo

```sh
git clone https://github.com/IBM/ibm-watson-embed-charts.git
cd ibm-watson-embed-charts/charts
```

The containers deployed in this chart come from the IBM entitled registry. You must create a Secret with credentials to pull from the IBM entitled registry. ibm-entitlement-key is the default name, but this can be changed by updating the imagePullSecrets value.

An example command to create the pull secret:

```sh
 oc create secret docker-registry ibm-entitlement-key \
  --docker-server=cp.icr.io \
  --docker-username=cp> \
  --docker-password=$IBM_ENTITLEMENT_KEY \
  --docker-email=<your-email>
```

Helm charts have configurable values that can be set at install time. Refer to the base values.yaml for documentation and defaults for the values. Values can be changed using `--set` or using YAML files specified with `-f/--values`. Here we are setting values using `--set` parameter

```sh
helm install 
--set license=true \
--set nameOverride=stt \
--set models.enUSTelephony.enabled=false \
--set postgres.host="postgresql-release-hl" \
--set postgres.user="postgres" \
--set postgres.password=$POSTGRES_PASSWORD \
--set objectStorage.endpoint=$S3_ENPOINT_URL \
--set objectStorage.region=$S3_REGION \
--set objectStorage.bucket=$S3_BUCKET_NAME \
--set objectStorage.accessKey=$S3_ACCESS_KEY \
--set objectStoragesecretKey=$S3_SECRET_KEY \
stt-release ./ibm-watson-stt-embed
```
