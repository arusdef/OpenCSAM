#!/bin/bash -e
# This script allows for creation of an index.

ES_URL=${ES_URL:-localhost:9200}
ES_INDEX=${ES_INDEX:-testing}
MAPPING_FILE=${MAPPING_FILE:-mapping-content.json}
TIMEOUT=5

echo
echo "Elasticsearch URL [$ES_URL]"
echo "Elasticsearch Index [$ES_INDEX]"

function print_indices {
  curl -k -XGET "$ES_URL/_cat/indices?v&s=index" -s | grep "health\|$ES_INDEX"
}

printf "\n\n------------------------\n"
printf "Creating $ES_INDEX index"
printf "\n--------------------------\n"

curl -k -XPUT "$ES_URL/$ES_INDEX?pretty=true" -H "Content-Type: application/json" -d @"$MAPPING_FILE"

sleep "$TIMEOUT"

printf "\n\n------------------------\n"
printf "Printing out indices"
printf "\n--------------------------\n"

print_indices

echo
