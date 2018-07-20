#!/bin/bash

ES_URL=${ES_URL:-elasticsearch:9200}
ES_INDEX=${ES_INDEX:-content}
ES_TYPE=${ES_TYPE:-article}
LOG_LEVEL=${LOG_LEVEL:-INFO}
CLOSESPIDER_PAGECOUNT=${CLOSESPIDER_PAGECOUNT:-100}

for spider in $(docker run -it --rm --entrypoint "scrapy" scrapy-crawlers list | grep web_ | tr -d '\r'); do
    echo "Crawling for $spider"
    docker run -it --rm --link=elasticsearch --net=elastic \
    -e "ES_URL=${ES_URL}" \
    -e "ES_INDEX=${ES_INDEX}" \
    -e "ES_TYPE=${ES_TYPE}" \
    scrapy-crawlers $spider \
    -s "LOG_LEVEL=${LOG_LEVEL}" \
    -s "CLOSESPIDER_PAGECOUNT=${CLOSESPIDER_PAGECOUNT}"
done
