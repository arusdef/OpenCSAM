# Useful Scripts

***

## mapping-create.sh shell script

A shell script to create a `mapping (schema)` in Elasticsearch DB. If you do not specify a mapping, Elasticsearch will by default generate one dynamically when detecting new fields in documents during indexing. However, this dynamic mapping generation comes with a few caveats: detected types might not be correct, uses default analyzers and settings for indexing and searching.

The schema in Elasticsearch is a mapping that describes the the fields in the JSON documents along with their data type, as well as how they should be indexed in the Lucene indexes that lie under the hood. Because of this, in Elasticsearch terms, we usually call this schema a “mapping”.

`mapping-create.sh` script should be used on a newly created database only. If you need to update an existing DB which already has some data, please use `mapping-update.sh` script (described below).

For the `content` index:

```sh
env "ES_URL=https://xxx:yyy@elastic.opencsam.enisa.europa.eu" "ES_INDEX=content" "MAPPING_FILE=mapping-content.json" ./mapping-create.sh
```

And for the `twitter` index:

```sh
env "ES_URL=https://xxx:yyy@elastic.opencsam.enisa.europa.eu" "ES_INDEX=content" "MAPPING_FILE=mapping-twitter.json" ./mapping-create.sh
```

***

## mapping-update.sh shell script

A script to update index with a specified mapping. The script allows for redefinition of existing index by defining new index with new schema, copying there old data (using _reindex) and then deleting and defining old index once again to finally copy data into old-new index.

For the `content` index:

```sh
env "ES_URL=https://xxx:yyy@elastic.opencsam.enisa.europa.eu" "ES_INDEX=content" "MAPPING_FILE=mapping-content.json" ./mapping-update.sh
```

And for the `twitter` index:

```sh
env "ES_URL=https://xxx:yyy@elastic.opencsam.enisa.europa.eu" "ES_INDEX=content" "MAPPING_FILE=mapping-twitter.json" ./mapping-update.sh
```

The mapping file and temporary index can be defined as well as `ES_INDEX_TMP` and `MAPPING_FILE` if required.

***

## pdf-documents-light.sh

This script allows for creation of an light version of `pdf_documents` index which contains a big blobs of text and is very heavy to process and render in Kibana.

```sh
env "ES_URL=https://xxx:yyy@elastic.opencsam.enisa.europa.eu" "ES_INDEX=pdf_documents" "ES_INDEX_DEST=pdf_documents_light" ./pdf-documents-light.sh
```

***

## stresstest.py

A python script based on [locust](https://locust.io/) to stress test a search performance at ES database.

You can run `locust` web UI where you can manage your stress tests

```sh
locust -f stresstest.py --host=http://localhost:9200
```

Alternatively, you can run it headless

```sh
env "ES_INDEX=content" locust -f stresstest.py --host=http://localhost:9200 -c 200 -r 50 --run-time 5m --no-web
```

where `-c` specifies the number of Locust users to spawn, and `-r` specifies the hatch rate (number of users to spawn per second).
