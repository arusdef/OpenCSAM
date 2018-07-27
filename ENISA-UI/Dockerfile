FROM node:8.11.3-slim

RUN apt-get update && apt-get install -y bzip2 python

RUN npm install -g npm@latest
RUN npm install -g yarn@latest

RUN npm install -g @angular/cli@latest
RUN npm install -g protractor@latest
RUN npm install -g typescript@latest

WORKDIR /opt/webapp
COPY . /opt/webapp/.

RUN ng update @angular/cli
RUN npm install
RUN webdriver-manager update --ignore_ssl && ./scripts/protractor.sh

EXPOSE 4200

CMD ng serve ---host 0.0.0.0 --disable-host-check true