FROM python:3-jessie

RUN pip install Scrapy ScrapyElasticSearch scrapyd

RUN mkdir -p /etc/scrapyd
RUN echo "[scrapyd]" >> /etc/scrapyd/scrapyd.conf
RUN echo "bind_address=0.0.0.0" >> /etc/scrapyd/scrapyd.conf

EXPOSE 6800
CMD ["scrapyd"]