# Instructions

## Docker 
Pull the [Docker image](https://hub.docker.com/r/mochar/wgcna/), and create and run a container. 

## Manual
#### Clone git
`git clone git@github.com:mochar/wgcna.git`

#### Prepare data folder:
Create the data folder:
`mkdir /opt/wgcna`

set write permission for user:
`sudo chown -R user:user /opt/wgcna`

#### In www folder:
Install npm if it is not installed.

Install required packages:
`npm install`

From now on run the web server with:
`npm run dev`

#### In api folder:
Install any missing dependencies that are causing errors.

From now on run the api server with:
`FLASK_APP=app/__init__.py flask run`

#### Open webtool:
open `localhost:4000` in your webbrowser.
