FROM python:3.6.5-jessie

RUN pip install Scrapy==1.5.0 fake-useragent==0.1.10 \
beautifulsoup4==4.6.0 elasticsearch==6.3.0 python_dateutil==2.7.3

ENV ES_URL=
ENV ES_INDEX=
ENV ES_TYPE=
ENV RSS_LINK=
ENV RSS_LABEL=

WORKDIR /opt/spiders
COPY . /opt/spiders
RUN pip install -r requirements.txt

ENTRYPOINT [ "scrapy", "guard_crawl" ]
CMD [ "rss_crawler" ]