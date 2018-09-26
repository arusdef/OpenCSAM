FROM node:8.11.3-slim

RUN apt-get update && apt-get install -y bzip2 python

RUN npm cache verify
RUN npm install -g @angular/cli@1.7.3

WORKDIR /opt/webapp
COPY . /opt/webapp/.

RUN npm install

RUN ng build --prod --build-optimizer
WORKDIR /opt/webapp/dist

EXPOSE 4200

CMD python -m SimpleHTTPServer 4200