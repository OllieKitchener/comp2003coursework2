# comp2003coursework2
Implementation of a Microservice

This repo contains a profile microservice which records sample data and allows for user input, which can be performed through swagger.

Using Docker-
1.
run this following command in your powershell: 

docker pull oliverkitchener/trail-profile-service:latest

2.
run this following command in your powershell:

docker run -p 8080:8080 oliverkitchener/trail-profile-service

3.
Swagger can be accessed through http://localhost:8080/api/ui
API can be accessed through http://localhost:8080/api/profiles
