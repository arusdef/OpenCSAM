# Web Scraping

## Useful Resources

[The Hitchhiker’s Guide to Python](http://docs.python-guide.org/en/latest/)

[Scrapy Documentation](https://docs.scrapy.org/en/latest/intro/tutorial.html)

[Scraping Tips and Tricks](https://hackernoon.com/web-scraping-tutorial-with-python-tips-and-tricks-db070e70e071)

[RSS Specification](https://cyber.harvard.edu/rss/rss.html)

[CSS3 Selectors](https://www.w3.org/TR/selectors-3/)

## Web Scraping Tutorial

### Intro

Web scraping is a technique used to extract data from websites through an automated process.

`Scrapy` is a web scraping and data extracting framework written in `Python` (programming language).

In most cases scraping of a web site is a very straightforward process but requires a manual inspection of HTML code of the website to access the classes and IDs you need. There are a few useful tools which should help with it `Google Chrome` and `scrapy shell`.

The code is organized in modules and classes so it makes easier to work with it. Spiders are classes that you define and that Scrapy uses to scrape information from a website. You can find them at `/scrapy_crawlers/spiders`. Run `scrapy list` in the command line inside the project to get a full list of available _spiders_.

Selectors are patterns that match against elements in a DOM (Document Object Model) tree, and as such form one of several technologies that can be used to select nodes in an XML (HTML) document. CSS (Cascading Style Sheets) is a language for describing the rendering of HTML documents. CSS uses Selectors for binding style properties to elements in the document. Selectors can also be used to select a set of elements, or a single element from a set of elements, by evaluating the expression across all the elements in a subtree.

Each spider (in most cases) requires 5 key elements (selectors) to retrieve the content from a web resource.

1. `links_to_articles_query` - CSS selector which uniquely identifies a path to a link to articles (catalogue web page)
1. `links_to_pages_query` - CSS selector which uniquely identifies a path to a link to pages (catalogue web page)
1. `extract_title_query` - CSS selector to retrieve a title (article web page)
1. `extract_datetime_query` - CSS selector to retrieve a timestamp (article web page)
1. `extract_content_query` - CSS selector to retrieve a content (article web page)

### Getting CSS Selectors

1. Open Chrome browser
1. Go to a desired web page
1. Open a developers console (View -> Developer -> Developer Tools)

In order to select `css path` in the developer console do `(right click on the element in Elements Window) > Copy > Copy selector`

Alternatively, you can call a JS function to retrieve a full path to the element

```js
crumb = function(node) {
    var idOrClass = (node.id && "#" + node.id) || ("" + node.classList && (" " + node.classList).replace(/ /g, "."));
    return node.tagName.toLowerCase() + idOrClass;
};
crumbPath = function(node) {
    return node.parentNode ? crumbPath(node.parentNode).concat(crumb(node)) : [];
};
crumbPath($0);
```

As a result you might get something like (this example is for `links_to_pages_query`)

```text
body > main > div > div > div.g-u-17-24.ml_g-u-1 > div > div > div > div > div.pagination > ul > li:nth-child(12) > a
```

which sometimes needs to be cleaned up. A general recommendation here is to get rid of any overcomplicated class names and indexes. So, you might end up with something like `body > main div.pagination > ul > li > a` instead.

### Scrapy Shell

1. Open a terminal
1. Go to the ${project}/scrapy_crawlers
1. Run `scrapy shell __url__` (or `fetch('__url__')` if you are already in the console)
1. Call `response.css('__css__selector__').extract()` to see what kind of results you will get back

## Prepare Environment

```sh
pip install -r requirements.txt
```

## Run Spiders

```sh
env "ES_URL=http://localhost:9200" "ES_INDEX=websites" "ES_TYPE=article" scrapy guard_crawl web_securelist -s "LOG_LEVEL=INFO"
```

where `guard_crawl` is a custom command which is specified to exit with a `non 0` status on error.

## Build Spiders for Docker

```sh
make # to build locally
make push # to build locally and push to the docker repository
```

## Run Spiders in Docker

### When ES database is local (docker)

```sh
docker run -it --rm --link elasticsearch --net elastic -e "RSS_LINK=http://feeds.arstechnica.com/arstechnica/security" -e "RSS_LABEL=arstechnica" scrapy-crawlers rss_crawler -s "ES_URL=elasticsearch:9200" -s "ES_INDEX=content" -s "ES_TYPE=article" -s "LOG_LEVEL=INFO"
```

```sh
docker run -it --rm --link elasticsearch --net elastic scrapy-crawlers web_politico -s "ES_URL=elasticsearch:9200" -s "ES_INDEX=content" -s "ES_TYPE=article" -s "LOG_LEVEL=INFO" -s "CLOSESPIDER_PAGECOUNT=50"
```

## Twitter Scraping

Twitter scraper can be found at twitter-crawlers/ folder. The spider uses twitter API to retrieve a specified number of tweets for each account. Accounts which are required to be scraped can be specified as configuration parameters:

1. ES_URL - ES URL, e.g. `https://xxx:yyy@elastic.opencsam.enisa.europa.eu`
1. ES_INDEX - ES Index, e.g. `twitter`
1. ES_TYPE - ES type, e.g. `tweet`
1. TW_CONSUMER_KEY - twitter consumer key
1. TW_CONSUMER_SECRET - twitter consumer secret
1. TW_ACCESS_TOKEN_KEY - twitter access token
1. TW_ACCESS_TOKEN_SECRET - twitter secret token

Twitter access credentials can taken from a twitter dev page (!you need a dev account for it!).

In order to update a list of twitter ids you need to edit `Jenkinsfile` pipeline script on Jenkins.