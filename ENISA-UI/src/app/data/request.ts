export const request_json= {
    "size": 10,
    "sort": [
      {
        "published": {
          "order": "desc",
          "unmapped_type": "boolean"
        }
      }
    ],
    "query": {
      "bool": {
        "must": [
          {
            "query_string": {
              "query": "",
              "analyze_wildcard": true,
              "default_field": "*"
            }
          },
          {
            "function_score": {
                "functions": [
              ]
            }
        }
          ,
          {
            "range": {
              "published": {
                "gte": 1523626875449,
                "lte": 1531402875449,
                "format": "epoch_millis"
              }
            }
          }
        ]
      }
    }
  }