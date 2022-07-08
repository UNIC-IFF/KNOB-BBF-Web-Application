<p align="center"><img src="https://github.com/UNIC-IFF/BBF-FLASK-API/blob/main/figs/bbf_api_logo.png" /></p>


# Overview
The Blockchain Benchmarking Framework will focus on the development of a user-friendly UI that abstracts the underlying complexities of blockchain technology and allows the user to have a seamless and easy interaction with the framework. The goal of the project is to enable usability for: (a) the demand (i.e., developers, technical teams, managers), (b) the supply (i.e., organizations and companies that provides data and/or services and wish to adopt blockchain technology) and (c) the academic (i.e., researchers, students, educators).

# Instructions

To execute the FLASK API you should execute with admin privileges the initialize.sh ( `sudo ./initialize.sh` ) file under the main folder. 
In case the css and Js is not working properly please execute in the terminal the following commands:
 1. `docker exec -it bbf-gui-apis /bin/bash`
 2. `npm install`
 3. `gulp`

The swagger URL is the: http://172.19.0.2/swagger
The main page is the: http://172.19.0.2/home
For each API type the prefered network. The list of the avialable networks can be seen by the "list" API.

# Model Architecture

<p align="center"><img src="https://github.com/UNIC-IFF/BBF-FLASK-API/blob/main/figs/architecture.png" /></p>

# Files description
- app.py: the main file that operates the flask api and combines all the components
- defaults.env: enviroment viariables for the Docker/FLASK API (dockerized) 
- docker-compose: The docker-compose file that enables docker-compose command and builds the docker filer
- static/swagger.json: Swagger is a set of open-source tools built around the OpenAPI Specification that can help design, build, document and consume REST APIs. swagger.json file is required to parameterize the apis and return the outputs.
- static/request_api.py: Is responsible for the controller (./control.sh) of the BBF. It executes the basic commands
- static/docker_api.py: Contains docker related apis (e.g., uptime, network, memory usage etc)
- static/traffic_monitor_apis.py: Contains traffic and node related APIs. It can create traffic, return node's information and account information.

## Contributors
- Marios Touloupos ( @mtouloup ) - UBRI Fellow Researcher / PhD Candidate, University of Nicosia - Institute for the Future ( UNIC -IFF)
- George Michoulis ( @gmixoulis ) - Full Stack / Blockchain Developer, University of Nicosia - Institute for the Future ( UNIC -IFF)
- Evgenia Kapassa ( @ekapassa ) - Researcher / PhD Candidate, University of Nicosia - Institute for the Future ( UNIC -IFF)

# Research Team
* Marios Touloupou (@mtouloup) [ touloupos.m@unic.ac.cy ]
* George Michoulis (@gmixoulis) [ michoulis.g@unic.ac.cy ]
* Evgenia Kapassa (@ekapassa) [ kapassa.e@unic.ac.cy ]
* Klitos Christodoulou [ christodoulou.kl@unic.ac.cy ]
* Elias Iosif [ iosif.e@unic.ac.cy ]

## Acknowledge
This work is funded by the XRPL Grants. The XRPL Grants program seeks to enable others to build inclusive standards leveraging the XRP Ledger’s open source technology and further innovate in the Internet of Value.
Link: [XRPL Grants](https://xrplgrants.org/)


## About IFF

IFF is an interdisciplinary research centre, aimed at advancing emerging technologies, contributing to their effective application and evaluating their impact. The general mission at IFF is to educate leaders, develop knowledge and build communities to help society prepare for a future shaped by transformative technologies. The institution has been engaged with the community since 2013 offering the World’s First Massive Open Online Course (MOOC) on blockchain and cryptocurrency for free, supporting the community and bridging the educational gap on blockchains and digital currencies.
