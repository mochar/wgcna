# Installation 

## Docker 
Install [Docker Compose](https://docs.docker.com/compose/install/), and run `(sudo) docker-compose up` in the root directory. 

## Manual
#### Clone git
`git clone git@github.com:mochar/wgcna.git`

#### In www folder:
Install npm if it is not installed.

Install required packages:
`npm install`

#### In api folder:
Install any missing dependencies that are causing errors.

#### Prepare data folder:
Create the data folder:
`mkdir /opt/wgcna`

set write permission for user:
`sudo chown -R user:user /opt/wgcna`

# Run instructions:
#### In www folder:
`npm run dev`

#### In api folder:
`export FLASK_APP=app/__init__.py`

`flask run`

#### Open webtool:
open `localhost:4000` in google chrome.
