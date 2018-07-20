#!/bin/bash -e
# This script allows for redefinition of existing index by defining new index with new schema, copying there old data
# (using _reindex) and then deleting and defining old index once again to finally copy data into old-new index.
# This might not work so good with big indexes, it is possible to apply this strategy using _snapshot API.
# Make sure you understand what this script does before running it, it could be very destructive.
# In theory index _close / _open should allow for adding a new analyzer, but this approach did not work for me.

ES_URL=${ES_URL:-localhost:9200}
ES_INDEX=${ES_INDEX:-testing}
ES_INDEX_TMP="$ES_INDEX-$(openssl rand -hex 4)-$(date +%Y.%m.%d)"
MAPPING_FILE=${MAPPING_FILE:-mapping-content.json}
TIMEOUT=5

echo
echo "Elasticsearch URL [$ES_URL]"
echo "Elasticsearch Index [$ES_INDEX]"
echo "Elasticsearch Temporary Index [$ES_INDEX_TMP]"

function print_indices {
  curl -k -XGET "$ES_URL/_cat/indices?v&s=index" -s | grep "health\|$ES_INDEX"
}

function should_continue {
  echo; echo "Do you wish to continue?"
  select yn in "Status" "Yes" "No"; do
  case $yn in
      "Status" ) echo; print_indices; echo;;
      "Yes" ) break;;
      "No" ) exit;;
  esac
  done
}

printf "\n\n------------------------\n"
printf "Coping from $ES_INDEX to $ES_INDEX_TMP"
printf "\n--------------------------\n"

curl -k -XPOST --fail "$ES_URL/_reindex?pretty=true&wait_for_completion=false" -H "Content-Type: application/json" -d"
{
  \"source\": {
    \"index\": \"$ES_INDEX\"
  },
  \"dest\": {
    \"index\": \"$ES_INDEX_TMP\"
  }
}"

sleep "$TIMEOUT"
echo; print_indices;

# Wait for the confirmation to proceed
should_continue

printf "\n\n------------------------\n"
printf "Deleting original $ES_INDEX index"
printf "\n--------------------------\n"

curl -k -XDELETE --fail -H "Content-Type: application/json" "$ES_URL/$ES_INDEX?pretty=true"

sleep "$TIMEOUT"

printf "\n\n------------------------\n"
printf "Creating $ES_INDEX index"
printf "\n--------------------------\n"

curl -k -XPUT "$ES_URL/$ES_INDEX?pretty=true" -H "Content-Type: application/json" -d @"$MAPPING_FILE"

sleep "$TIMEOUT"

printf "\n\n------------------------\n"
printf "Coping from $ES_INDEX_TMP to $ES_INDEX"
printf "\n--------------------------\n"

curl -k -XPOST --fail "$ES_URL/_reindex?pretty=true&wait_for_completion=false" -H "Content-Type: application/json" -d"
{
  \"source\": {
    \"index\": \"$ES_INDEX_TMP\"
  },
  \"dest\": {
    \"index\": \"$ES_INDEX\"
  }
}"

sleep "$TIMEOUT"

printf "\n\n------------------------\n"
printf "Printing out indices"
printf "\n--------------------------\n"

print_indices

echo
