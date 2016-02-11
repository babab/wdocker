# wdocker vars:

#wd# docker = docker
#wd# name = many_commands
#wd# build = {docker} build -t {name} .
#wd# run = {docker} run -it --name {name} {name}

# wdocker commands:

#wd# build: {build}
#wd# run: {run}
#wd# shell: {docker} exec -it {name} bash
#wd# start: {docker} start {name}
#wd# stop: {docker} stop {name}
#wd# attach: clear && {docker} attach {name}
#wd# build-and-run: {build} && {run}
#wd# rm: {docker} rm {name}
#wd# ip: echo -n IP: && {docker} exec {name} ip addr | grep 172

# needs one or more arguments
#wd# exec: {docker} exec -it {name}

FROM debian:latest
CMD watch ps aux
