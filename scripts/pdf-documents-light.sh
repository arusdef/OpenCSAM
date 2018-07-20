#!/bin/bash -e
# This script allows for creation of an index.

ES_URL=${ES_URL:-localhost:9200}
ES_INDEX=${ES_INDEX:-pdf_documents}
ES_INDEX_DEST=${ES_INDEX_DEST:-pdf_documents_light}
TIMEOUT=5

echo
echo "Elasticsearch URL [$ES_URL]"
echo "Elasticsearch Index [$ES_INDEX]"

function print_indices {
  curl -k -XGET "$ES_URL/_cat/indices?v&s=index" -s | grep "health\|$ES_INDEX"
}

printf "\n\n------------------------\n"
printf "Coping from $ES_INDEX to $ES_INDEX_DEST"
printf "\n--------------------------\n"

curl -k -XPOST --fail "$ES_URL/_reindex?pretty=true&wait_for_completion=false" -H "Content-Type: application/json" -d"
{
  \"source\": {
    \"index\": \"$ES_INDEX\",
    \"_source\": [\"filename\", \"keywords\", \"recommendations\", \"summary\", \"title\", \"topics\"]
  },
  \"dest\": {
    \"index\": \"$ES_INDEX_DEST\"
  }
}"

sleep "$TIMEOUT"

printf "\n\n------------------------\n"
printf "Printing out indices"
printf "\n--------------------------\n"

print_indices

echo
