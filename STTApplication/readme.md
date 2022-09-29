## STT Client Application
In this tutorial you will build and run a Java Spring Boot web application that relies on Watson Speech-to-Text (STT) as a back-end service. The application code can be used as a starting point when developing your own speech application.

The application demonstrates two interfaces that a client program can use to leverage Watson STT.
- **REST interface.** This is used for batch processing, where the client sends audio files to the Watson STT and recieves transcriptions synchronously.
- **WebSocket interface.** This can be used for streaming use cases, where the the communication happens asynchronously.

In order to use this tutorial, you need to have first deployed an instance of Watson STT on a Kubernetes or OpenShift cluster.

### Architecture diagram

![Diagram](architecture.png)
 
### Prerequisites
- Docker is installed on your local machine.
- Java 17 is installed.
- Eclipse (optional) is installed, if you want to customize the application.
- You have deployed Watson STT on a Kubernetes or OpenShift cluster.

### Get the sample code
Clone the following GitHub repository.
```
git clone https://github.com/ibm-build-labs/Watson-NLP
```
This repository contains code that is used in this tutorial.

## Steps to run on your local machine

Follow the steps below to run the application on your local machine. In a subsequent section are instructions for running it on the same Kubernetes or OpenShift cluster where the Watson STT service is running.

### 1. Build
Go to the directory that contains sample code for this tutorial.
```
cd Watson-NLP/STTApplication
```
A Maven wrapper is used here to build and package the application.
```
./mvnw clean package
```
The application will be packaged in JAR file: `target/STTApplication-0.0.1-SNAPSHOT.jar`.

### 2. Test
Login Kubernetes cluster and expose the STT service endpoint.
```
kubectl port-forward svc/install-1-stt-runtime 1080
```
Set the following environment variable. The Java application will use this to find the STT service.
```
export STT_SERVICE_ENDPOINT=127.0.0.1:1080
```
Run the application.
```
java -jar target/STTApplication-0.0.1-SNAPSHOT.jar
```
The application will listen on port 8080. Access the application in your browser using the following URL.
```
http://localhost:8080
```

## Run in Kubernetes
As an alternative to running the application on your local machine, in this 

### 1. Build an Image.
Here is a simple docker file we used to build a docker image.
```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```
- Before building the image please execute the below command to package the application
```
./mvnw clean package
```

- Build the image with the below command. I am using ibm container registry to push the image. You can choose a repository on your own.
```
docker build . -t us.icr.io/watson-core-demo/stt-web-application:v1
```
- Push the image to upstream
```
docker push us.icr.io/watson-core-demo/stt-web-application:v1
```
### 2. Deploy
We are creating two Kubernetes resources here, deployment and a service. In deployment.yaml file you need to modify two things
 - Image location
 - Environmental variable STT_SERVICE_ENDPOINT

Here is a sample deployment.yaml file and highlighted the text you might want to replace.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stt-web-app
spec:
  selector:
    matchLabels:
      app: stt-web-app
  replicas: 1
  template:
    metadata:
      labels:
        app: stt-web-app
    spec:
      containers:
      - name: stt-web-app
        image: us.icr.io/watson-core-demo/stt-web-application:v1
        resources:
          requests:
            memory: "500m"
            cpu: "100m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
          - name: STT_SERVICE_ENDPOINT
            value: "install-1-stt-runtime:1080"
        ports:
        - containerPort: 8080
```

Get STT service name from the Kubernetes cluster you have deployed your STT Serving. Here is an example. In my case my STT service name is install-1-stt-runtime and port is 1080 for non tls and for tls 1443
```
kubectl get svc 
```
Output
```
NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
install-1-stt-runtime         NodePort    172.21.206.51    <none>        1080:30280/TCP,1443:32753/TCP   14d
install-1-tts-runtime         NodePort    172.21.199.140   <none>        1080:31439/TCP,1443:30824/TCP   14d
```

Here I am creating a clusterIP service exposing in port 8080, Here is the yaml file
```
apiVersion: v1
kind: Service
metadata:
  name: stt-web-app
spec:
  type: ClusterIP
  selector:
    app: stt-web-app
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
```

deploy kubernetes resource by executing the below command.
```
kubectl apply -f /deployment/
```
### 3. Test 

Check that the pod and service are running.
```
kubectl get pods
```
```
NAME                                           READY   STATUS    RESTARTS   AGE
stt-web-app-64d9df8f49-4fm97                   1/1     Running   0          25h
```
```
kubectl get svc 
```
```
NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
stt-web-app                   ClusterIP   172.21.238.164   <none>        8080/TCP                        25h
```

To access the app, you need to do a port-forward
```
kubectl port-forward svc/stt-web-app 8080
```

you can access the app at http://localhost:8080

## Understanding the Application Code

The Feign library is used to make REST calls. Below is the list of libraries that are used for this application.
```
<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-thymeleaf</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-openfeign</artifactId>
		</dependency>
		<dependency>
		  <groupId>io.github.openfeign</groupId>
		  <artifactId>feign-httpclient</artifactId>
		</dependency>
</dependencies>
```

