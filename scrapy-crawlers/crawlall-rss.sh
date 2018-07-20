#!/bin/bash

read -r -d '' feeds <<- EOD
https://www.bleepingcomputer.com/feed/,bleepingcomputer
http://feeds.arstechnica.com/arstechnica/security,arstechnica
https://threatpost.com/feed/,threatpost
https://www.darkreading.com/rss_simple.asp,darkreading
https://www.csoonline.com/index.rss,csoonline
http://feeds.feedburner.com/securityweek,securityweek
https://securityaffairs.co/wordpress/feed,securityaffairs
https://nakedsecurity.sophos.com/feed/,nakedsecurity
https://securelist.com/feed/,securelist,securelist
http://feeds.feedburner.com/SecurityIntelligence,securityintelligence
http://feeds.feedburner.com/bankinfosecurity/com,bankinfosecurity
https://feeds.feedburner.com/CiscoBlogSecurity,cisco
https://blog.malwarebytes.com/feed,malwarebytes
http://www.itsecurityguru.org/feed,itsecurityguru
https://www.euractiv.com/?feed=newsletter,euractiv
https://www.politico.com/rss/morningcybersecurity.xml,politico
https://www.wired.com/feed/category/security/latest/rss,wired
https://www.secureworks.com/rss?feed=research&category=threat-analysis,secureworks
http://feeds.trendmicro.com/Anti-MalwareBlog,trendmicro
http://feeds.feedburner.com/TheHackersNews,thehackernews
https://www.ncsc.gov.uk/feeds/reports.xml,ncsc
http://feeds.feedburner.com/eset/blog,welivesecurity
http://feeds.feedburner.com/securityweekly/XBIC,securityweekly
https://cert.europa.eu/rss?type=category&id=CERT-LatestNews&language=en&duplicates=false,cert
EOD

ES_URL=${ES_URL:-elasticsearch:9200}
ES_INDEX=${ES_INDEX:-content}
ES_TYPE=${ES_TYPE:-article}
LOG_LEVEL=${LOG_LEVEL:-INFO}
CLOSESPIDER_PAGECOUNT=${CLOSESPIDER_PAGECOUNT:-20}

for feed in $feeds; do
    echo "Crawling for $feed"
    docker run -it --rm --link=elasticsearch --net=elastic \
    -e "ES_URL=${ES_URL}" \
    -e "ES_INDEX=${ES_INDEX}" \
    -e "ES_TYPE=${ES_TYPE}" \
    -e "RSS_LINK=$(echo $feed | cut -d, -f1)" \
    -e "RSS_LABEL=$(echo $feed | cut -d, -f2)" \
    scrapy-crawlers rss_crawler \
    -s "LOG_LEVEL=${LOG_LEVEL}"
done
