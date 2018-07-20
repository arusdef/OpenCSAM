#!/bin/bash -e
# This script creates repository in Elasticsearch database to backup data

ES_URL=${ES_URL:-localhost:9200}
HDFS_URL=${ES_URL:-localhost:9000}
TIMEOUT=5

printf "\n\n------------------------\n"
printf "Creating hdfs repository"
printf "\n--------------------------\n"

curl -XPUT "$ES_URL/_snapshot/enisa_repository?pretty" -H "Content-Type: application/json" -d "
{
  \"type\": \"hdfs\",
  \"settings\": {
    \"uri\": \"hdfs://hadoop-hadoop-hdfs-nn.hadoop:9000/\",
    \"path\": \"/elasticsearch/enisa_repository\"
  }
}"

printf "\n\n------------------------\n"
printf "Printing all repositories"
printf "\n--------------------------\n"

curl -XGET "$ES_URL/_snapshot?pretty" -H "Content-Type: application/json"

echo
