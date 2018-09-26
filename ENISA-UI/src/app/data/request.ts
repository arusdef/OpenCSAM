export const QueryFilter = function() {
  return {
    "size":500,
    "sort": [
      {
        "_score": {
          "order": "desc"
        }
        ,
        "published": {
          "order": "desc",
          "unmapped_type": "boolean"
        }
      }
    ],
    "query": {
      "bool": {
        "must": []
      }
    },
    "highlight" : {
      "pre_tags" : ["<b>"],
      "post_tags" : ["</b>"],
      "fields" : {
          "title.*" : {
            "fragment_size" : 600, "number_of_fragments" : 1
          },
          "content.*": {
            "fragment_size" : 600, "number_of_fragments" : 1
          },
          "recommendations": {
            "fragment_size" : 600, "number_of_fragments" : 1
          },
          "summary": {
            "fragment_size" : 600, "number_of_fragments" : 1
          },
          "full_text.*": {
            "fragment_size" : 600, "number_of_fragments" : 1
          }
      }
    }
  }

}
