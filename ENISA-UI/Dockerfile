FROM node:8.11.3-slim

RUN npm i -g yarn
RUN npm install -g @angular/cli@latest

RUN yarn global add rxjs@^5.0.1
RUN yarn global add typescript
RUN yarn global add tslint
RUN yarn global add protractor
RUN yarn global add node-sass

RUN apt-get update && apt-get install -y bzip2
RUN npm i npm@latest -g

WORKDIR /opt/webapp
COPY . /opt/webapp/.
RUN npm install
RUN webdriver-manager update --ignore_ssl && ./scripts/protractor.sh

EXPOSE 4200

CMD ng serve -H 0.0.0.0 --disable-host-check true