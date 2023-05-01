
# Contributor's Guide

NOTE CI/CD Pipeline is not currently functional due to some error in bitops pipeline, work on creating custom terrafom pipeline is running

## Setting the project in your local

### Initial Steps

1. Install **python3** and **pip** on your local machine or remote server where you want to deploy the above API (https://realpython.com/installing-python/).

2. Setup git on your machine (https://www.atlassian.com/git/tutorials/install-git)

3. Git clone the entire repo  in a suitable folder, by navigating to the place through terminal and running **git clone https://github.com/defi-os/defios-python-apis.git**

### Setup all Python dependencies in a virtual environment

1) Install virtualenv on your machine using **pip3 install virtualenv**

2) Make a virtual env by **virtualenv {virtual_env_name}** where virtual_env_name is the desired name of the virtual environment, in this example, we would take it as venv

3) In the same location, run **souce venv/bin/active**

4) Now, navigate through the terminal to inside the  folder where the repo is initialised and run **pip install -r requirements.txt** to setup all dependencies for the project.

### Setting up the API on your local

1) To continue forward, setup a local mongodb instance(https://www.prisma.io/dataguide/mongodb/setting-up-a-local-mongodb-database) on your machine or connect with a remote mongodb instance. **Add the host or url link for your mongodb server or local name in mainapi.py line no.18, mongoengine.connect(host="")(for remote db) or mongoengine.connect("")(for local instances).**

5) Run **python3 mainapi.py**, the flask application should start!!! 

Please reference https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04 for guideline on how to deploy this API to production using nginx and gunicorn or setup any custom config you wish to push into production.


## Issue Reporting

Please mention all steps to reproduce the issue, link any custom code that led to the issue, and mention any CLI errors you got within the issue itsel


