# Data Management

## Elasticsearch

A schema is a description of one or more fields that describes the document type and how to handle the different fields of a document.

Elasticsearch has the ability to be schema-less, which means that documents can be indexed without explicitly providing a schema.

If you do not specify a mapping, Elasticsearch will by default generate one dynamically when detecting new fields in documents during indexing. However, this dynamic mapping generation comes with a few caveats:

1. Detected types might not be correct.
1. Uses default analyzers and settings for indexing and searching.

By explicitly specifying the schema, we can avoid these problems.

1. scripts/mapping-content.json `content` index schema
1. scripts/mapping-twitter.json `twitter` index schema

In order to provide a mapping to Elasticsearch run commands described below.

### Fresh ES Database

If you've just created a database and there are no data and indices yet, please, run

```sh
# local setup
cd scripts
env "ES_URL=localhost:9200" "ES_INDEX=content" "MAPPING_FILE=mapping-content.json" ./mapping-create.sh
# remote setup
cd scripts
env "ES_URL=https://xxx:yyy@elastic.europa.eu" "ES_INDEX=content" "MAPPING_FILE=mapping-content.json" ./mapping-create.sh
```

### Existing ES Database

If the index has been created already, please, run

```sh
# local setup
cd scripts
env "ES_URL=localhost:9200" "ES_INDEX=content" "MAPPING_FILE=mapping-content.json" ./mapping-update.sh
# remote setup
cd scripts
env "ES_URL=https://xxx:yyy@elastic.europa.eu" "ES_INDEX=content" "MAPPING_FILE=mapping-content.json" ./mapping-update.sh
```

## Jenkins and Scraping Automation

[Jenkins](https://jenkins.io/)

Jenkins is an open source automation server. Jenkins can be used as a simple CI server or turned into the continuous delivery hub for any project. Jenkins can be easily set up and configured via its web interface, which includes on-the-fly error checks and built-in help.

Jenkins Pipeline is a suite of plugins which supports implementing and integrating continuous delivery pipelines into Jenkins. Pipeline provides an extensible set of tools for modeling simple-to-complex delivery pipelines "as code" via the Pipeline domain-specific language (DSL) syntax. The definition of a Jenkins Pipeline is written into a text file (called a Jenkinsfile) which in turn can be committed to a project’s source control repository.

For this project we are using Jenkins and Pipelines to automate web scraping and data ingestion. Currently, it is not used as a CI tool but it's functionality can be extended later.

[WEB Scrapers Jenkinsfile](scrapy-crawlers/Jenkinsfile)
[RSS Scrapers Jenkinsfile](scrapy-crawlers/Jenkinsfile-RSS)
[Twitter Scrapers Jenkinsfile](twitter-crawlers/Jenkinsfile)
[Topics Jenkinsfile](enisa-nlp/Jenkinsfile)

Create new pipeline jobs in Jenkins and copy-paste required Jenkinsfile into the `Script` field. All other fields will be filled in automatically. Keep in mind, that only the script should be modified as other updates might be overriden by the script.

## Kibana

[Kibana](https://www.elastic.co/products/kibana) lets you visualize your Elasticsearch data. Kibana core ships with the classics: histograms, line graphs, pie charts, sunbursts, and more.

[Kibana Tutorial – Part 1: Introduction](https://www.timroes.de/2015/02/07/kibana-4-tutorial-part-1-introduction/)

[Kibana Tutorial – Part 2: Discover](https://www.timroes.de/2015/02/07/kibana-4-tutorial-part-2-discover/)

[Kibana Tutorial – Part 3: Visualize](https://www.timroes.de/2015/02/07/kibana-4-tutorial-part-3-visualize/)

[Kibana Tutorial – Part 4: Dashboard](https://www.timroes.de/2015/02/07/kibana-4-tutorial-part-4-dashboard/)

Kibana dashboards are stored in `kibana/export.json`. Unfortunately, there is no way to automate dashboards import. Therefore it should be done manually. Go to `Kibana` -> `Management` -> `Saved Objects` -> `Import` and point it to the json file. Assign the indexes thoroughly.

If you update dashboards it might be a good idea to commit changes to git.
