# wdocker vars:

#wd# docker = docker
#wd# name = php7
#wd# ports = -p 127.0.0.1:80:80

#wd# build = {docker} build -t {name} .
#wd# run = {docker} run -d {ports} --name {name} {name}

# wdocker commands:

#wd# shell: {docker} exec -it {name} bash
#wd# start: {docker} start {name}
#wd# stop: {docker} stop {name}
#wd# init: {build} ;; {run}

FROM php:7-apache
COPY src/ /var/www/html/
