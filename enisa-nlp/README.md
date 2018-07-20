# NLP Research

***
## PDF documents

The [pdf_documents](../enisa-nlp/pdf_documents) directory contains the code to read and process the text extracted from the pdf files.

[read_data.py](../enisa-nlp/pdf_documents/read_data.py)
* Read the plain text extracted from the pdf files and return it in the pandas dataframe format.

[document_structure.py](../enisa-nlp/pdf_documents/document_structure.py)
* Find chapter titles and split the documents into separate chapters, paragraphs or lines.
* Return the chapter containing a summary or recommendations.
* Decorate the dataframe with additional fields.

[utils.py](../enisa-nlp/pdf_documents/utils.py)
* Methods and classes useful for NLP algorithms.



***
## Knowledge graph

The knowledge graph provided by ENISA is the back bone of the information hierarchy understanding that we implemented in Elasticsearch. Elasticsearch makes it possible to define synonyms which serve well for the purposes of the information hierarchy understanding.

The ability to update the knowledge graph / information hierarchy and subsequently export it into a synonym format that Elasticsearch will understand is one of the requirements. This can be done with the [knowledge_graph.py](../enisa-nlp/knowledge_graph/knowledge_graph.py) script. The script uses the knowledge graph entered in the [knowledge_graph.cfg](../enisa-nlp/knowledge_graph/knowledge_graph.cfg) configuration file in a text format as an input, and prints out the synonyms on screen.

The configuration file should be written in the following way:
* The term in brackets defines a section in the configuration file and corresponds to one of the main legs
from the knowledge graph, linked to the cyber security blob.
* The term that will be used for searching in elasticsearch is defined in the category variable.
* In case there are multiple synonyms or abbreviations for this term, a comma-separated string can be used.
* The subcategories variable defines the lower level of the knowledge graph.
* Parents are writen with an indent and children are written with an indent followed by a dot.

Example:

```
[threats]
category = Threats
subcategories =
  Web application attacks
  . Cross-Site Scripting, XSS
  . Local File Inclusion, LFI
  . Remote File Inclusion, RFI
  . SQL injection
  . Cross-Site Request Forgery, CSRF
```


* At the moment, the script prints the synonyms on screen which will have to be copy pasted. A more user-friendly future feature could be to devise an export method that will directly update the analyzer and reindex.
* One can even think of having this as a part of the web application, with an export button in place.



***
## Topic modelling

One of the components of the dashboard should be a daily (or weekly) summary of topics used in the recent news articles. The idea is to extract keywords from the news articles in an automated way, find clusters to obtain distict topic groups and present them in a dashboard. Ideally, not only the topics/keywords will be presented, but also links to relevant news articles from each cluster.

The [topic.py](../enisa-nlp/topic/topic.py) script finds the clusters of topics/keywords from the recent news articles and saves the keywords in the Elasticsearch database. The script is scheduled to run on a daily basis through [Jenkinsfile](../enisa-nlp/Jenkinsfile) and [Dockerfile](../enisa-nlp/Dockerfile). The docker container can be run in the following way.

```sh
docker run -it --rm --link=elasticsearch --net=elastic enisa-nlp
```

```sh
docker run -it --rm --link=elasticsearch --net=elastic -e "ES_URL=xxx/elasticsearch" -e "ES_PORT=80" -e "ES_USERNAME=yyy" -e "ES_PASSWORD=zzz" enisa-nlp
```

The following two models are implemented in the `topic.py` script.
* **Latent Dirichlet Allocation (LDA)** using word counts as a vector representation of the text.
* **Non-negative Matrix Factorization (NMF)** using TF-IDF scores as a vector representation of the text.

The `topic.py` script can be configured through environmental variables. The configurable parameters are:
* `NUM_CLUSTERS`: The number of clusters to find (default = 5).
* `NUM_KEYWORDS`: The number of keywords per cluster (default = 5).
* `MODEL`: The model to use (default = NMF).
* `INDEX_NEWS`: The Elasticsearch index of the news articles. This is where the input data will be obtained from.
* `DAYS_FROM_TODAY`: The number of days in the past, counted from today, that will be used as a starting day for reading the news articles from the database (default = 7).
* `INDEX_TOPICS`: The Elasticsearch index that will be used to store the resulting clusters of keywords (default = topics). The information is uplaoded using the `save_topics` method from [elastic.py](../enisa-nlp/enisa_elastic/elastic.py). There will be a separate field for each cluter holding an array of keywords.
* `MAX_DF`: The maximum document frequency corresponding to a word used by a vectorizer to consider this word for being part of the vector representation (default = 0.1).
* `MIN_DF`: The minimum document frequency corresponding to a word used by a vectorizer to consider this word for being part of the vector representation (default = 0.001).
* `MAX_FEATURES`: The maximum size of the vector representation (default = 1000). In general there is a lot different words used in the news articles. Typically, we observe O(1000) words. O(1000) works is also a typical amount of the news articles per week. Therefore, in order to prevent overfitting and improve convergence, it is benefitial to reduce the number of features (dimension of the vector representation).


As a future feature, ideally we would want to present a dashboard which includes direct links to relevant articles from each cluster. In order to make this happen, we need to load the keywords from the database and use them in a curl command to query the news articles. Such query should use an OR combination of the keywords and return let us say 10 highest score articles per each cluster from the last week. I am assuming there will be a script executed by the web application to do these steps (load keywords from the topics index, extract the keywords and write them in an OR combination into a curl query command, and execute this curl command in order to retreive the article news links to display in the dashboard).



***
## Supervised keyword extraction

Our original idea was to use supervised techniques to train models that will be able to assign topics/keywords to new news articles. To train a supervised model, one needs to have labeled data available. We were intending to use the following:
* Tags/topics from the pdf documents provided by ENISA. These tags/topics are incomplete and the dataset size is insufficient.
* Hashtags from twitter (or other social media). This is a nice idea, but we haven't had time to investigate this. There are two benefits this approach may provide: 1) Social media usually provide large-enough datasets for training, 2) New tags will appear automatically and you will not miss out on important topics.
* Term glossary from wikipedia (or other sources). Again, this is a rather limited dataset for training.
* Knowledge graph provided by ENISA. This is what we tried in the end.

The following procedure describes the way to use the knowledge graph as an input for supervised models:
  * The idea was to use the top-level categories as labels. We used a fulltext search to find the terms from the knowledge graph in the news articles and assign a label to each article based on that. Multiple labels can be assign to a single article.
  * Remove the terms from the knowledge graph from the articles. The models should understand the context and not simply use the exact same words for both features and labels.
  * Fit a model. Various models were tried, leading to unsatisfactory results.
  
See the [keywords3.ipynb](../notebooks/keywords3.ipynb) notebook for a detailed study of different models (naive bayes, random forests, support vector machines, logistic regression) and different vector representations (word counts, TF-IDF, n-grams, embedding vectors). The concusions are:
* The models based on the knowledge graph do not lead to satisfactory performance (accuracy, F1-score).
* The training leads to overfitting, i.e. further regularization/improvements are needed.
* Doing a fulltext search using the information hierarchy understanding, implemented through synonyms, already provides enough power to search for documents related to difference categories based on the knowledge graph. Therefore, we decided not to focus on the supervised models further. Instead, we are using the power of Elasticsearch directly, without the need to integrate modeling based on ohter tools.

The jupter notebook mentioned above is the most complete study we did. Apart from that, there are examples on how to do the modeling in the [examples](../enisa-nlp/examples) directory, in case somebody wants to continue the studies/development in the future.
