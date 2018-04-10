# Installation instructions
#### Clone git
`git clone git@github.com:mochar/wgcna.git`

#### In wgcna folder:
Checkout developtment branch: `git checkout layout`

#### In www folder:
Install npm if it is not installed.

Install required packages:
`npm install`

Run the development web server:
`npm run dev`

#### In api folder:
Set location of flask application:
`export FLASK_APP=app/__init__.py`

Run flask application:
`flask run`

Install any missing dependencies that are causing errors.

#### Prepare data folder:
Create the data folder:
`mkdir /opt/wgcna`

set write permission for user:
`sudo chown -R user:user /opt/wgcna`

#### Open webtool:
open `localhost:4000` in google chrome.

# Run instructions:
#### In www folder:
`npm run dev`

#### In api folder:
`export FLASK_APP=app/__init__.py`

`flask run`

#### Open webtool:
open `localhost:4000` in google chrome.
