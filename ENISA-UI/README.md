# ENISA Cyber Security Search Web User Interface

## Running in Development Mode

* Ensure you have Node v8.11.1 and NPM 6.4.0 installed.
 - Node installation instructions: https://www.npmjs.com/
* Install angular cli 
    npm install @angular/cli@1.7.3
* install required packages 
    npm install
* Run local build `ng serve`

## Running in Production Mode

1. Install docker from: https://www.docker.com/ - *Needs to be done only once per machine*
2. Execute `docker build -t webapp .`
3. Execute `docker run -d --rm --name webapp -p 4200:4200 webapp`
4. Access the application in your browser: `http://localhost:4200`
5. To stop the application: `docker kill webapp`
