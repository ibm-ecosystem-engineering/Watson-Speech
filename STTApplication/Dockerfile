# Universal Base Image (UBI)
FROM registry.access.redhat.com/ubi8/openjdk-17:1.14-4.1666624568

# Non-root, arbitrary user ID s
USER 1001

WORKDIR /usr/src/app

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar

EXPOSE 8080

ENTRYPOINT ["java","-jar","app.jar"]