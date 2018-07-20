FROM python:3.6.5-jessie

RUN pip install elasticsearch==6.3.0 tweepy==3.6.0 python_dateutil==2.7.3

# ENV ES_URL=
# ENV ES_INDEX=
# ENV ES_TYPE=

# ENV TW_CONSUMER_KEY=
# ENV TW_CONSUMER_SECRET=
# ENV TW_ACCESS_TOKEN_KEY=
# ENV TW_ACCESS_TOKEN_SECRET=
# ENV TW_LIMIT=
# ENV TW_ID=

WORKDIR /opt/twitter
COPY requirements.txt /opt/twitter/.
COPY twitter_crawl.py /opt/twitter/.

RUN pip install -r requirements.txt

ENTRYPOINT []
CMD [ "./twitter_crawl.py" ]