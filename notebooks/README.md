# Jupyter Notebooks

***
## Time decay

The [decay.ipynb](../notebooks/decay.ipynb) notebook demonstrates how to use a time decay function as a filter in Elasticsearch to push the most recent results to the top. Such filter is optionally available both in the Discover part of Kibana as well as in the web application. ENISA can adjust how fast an article will decay in time by editing "scale", "offset" and "decay" in the function. The following exponential time decay function is implemented:

```
                    "exp": {
                        "published": {
                            "origin": "now", 
                            "scale": "7d",
                            "offset": "7d", 
                            "decay" : 0.5 
                        }
                    }
```



***
## Popularity / trustworthiness of sources

The [popularity.ipynb](../notebooks/popularity.ipynb) notebook demonstrates how to boost the search results based on the popularity or trustworthiness of a source. This is implemented as a filter in Elasticsearch. Such filter should be optionally available both in the discover part of Kibana as well as in the web application.

The popularity of the sources is provided by ENISA directly. We got it as an excel sheet. The notebook above uses the information from that sheet, extracted manually into a string in one of the jupyter notebook cells. The notebook than automatically produces the function to be used in an Elasticsearch filter.

The popularity scores range between 0 (least popular) and 10 (most popular). If a source is missing in the list, 5 will be used by default. These numbers are used as a multiplication factor for the search result scores.

It may be that exploiting the full range between 1 and 10 is too strong and it could be considered to restrict to a smaller range around 5 in order to reduce the power of the popularity boosting. For example, one could use numbers between 2.5 and 7.5 with steps of 0.5, depending on ENISA wishes.

As a thought, one could think about a way to automatically update the Elasticsearch filter once this input file with popularity scores is updated. Jenkins can certainly help there.



***
## Feedback loop

The [feedback.ipynb](../notebooks/feedback.ipynb) notebook demonstrates how to implement the feedback loop. The final solution (web application) should display a like/unlike button next to each link. This button will then increase/decrease the magnitude of the weight stored in a dedicated feedback field.

NOTE: The commands from this notebook have to be extracted in curl format. These curl commands will then be executed if a button is pressed in the web application. Note that every query in Elasticsearch will have to use field_value_factor.



***
## Synonyms

The [synonyms2.ipynb](../notebooks/synonyms2.ipynb) and [synonyms3.ipynb](../notebooks/synonyms3.ipynb) notebooks demonstrate how to use synonyms in analyzers.
The synonyms work well for enhancing the Elasticsearch capabilities with information hierarchy understanding. In this way, we embed the information structure from the ENISA knowledge graph in the final solution.

