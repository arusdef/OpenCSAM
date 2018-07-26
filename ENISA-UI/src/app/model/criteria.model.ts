import {request_json} from './../data/request';
export interface ICriteria  {
    k_graph?:Boolean;
    time_decay ?:Boolean;
    p_resources ?:Boolean;
    news_articles?:Boolean;
    tweeter_feed?:Boolean;
    enisa_reports?:Boolean;
    enisa_recomend?:Boolean;
    keyword?:string;
}

export class Criteria implements ICriteria {
    k_graph?:Boolean=true;
    time_decay ?:Boolean;
    p_resources ?:Boolean;
    news_articles?:Boolean=true;
    tweeter_feed?:Boolean;
    enisa_reports?:Boolean;
    enisa_recomend?:Boolean;
    keyword?:string;

    constructor(params?:ICriteria){
        if (params) {
            this.k_graph= params.k_graph;
            this.time_decay=params.time_decay;
            this.p_resources =params.p_resources;
            this.news_articles=params.news_articles;
            this.tweeter_feed=params.tweeter_feed;
            this.enisa_reports= params.enisa_reports;
            this.enisa_recomend=params.enisa_recomend;
            this.keyword = params.keyword;

        }
    }

    setCriteria(criteria:Criteria)
    {
        let json =request_json;
        console.log("inside set criteria");
        console.log(json);

        debugger;
        
        //empty the array of functions 
        json.query.bool.must[1].function_score.functions = [];

        if(criteria.k_graph==true)
                 json.query.bool.must[0].query_string.default_field ="*.knowledge_graph";

        if(criteria.p_resources){
            json.query.bool.must[1].function_score.functions.push({
                "filter": {
                    "match": {
                        "resource_label": "arstechnica"
                    }
                },
                "weight": 1.6
            }, {
                "filter": {
                    "match": {
                        "resource_label": "bankinfosecurity"
                    }
                },
                "weight": 1.2
            }, {
                "filter": {
                    "match": {
                        "resource_label": "bleepingcomputer"
                    }
                },
                "weight": 1
            }, {
                "filter": {
                    "match": {
                        "resource_label": "csoonline"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "darkreading"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "euractiv"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "itsecurityguru"
                    }
                },
                "weight": 0.8
            }, {
                "filter": {
                    "match": {
                        "resource_label": "malwarebytes"
                    }
                },
                "weight": 1.6
            }, {
                "filter": {
                    "match": {
                        "resource_label": "nakedsecurity"
                    }
                },
                "weight": 1
            }, {
                "filter": {
                    "match": {
                        "resource_label": "politico"
                    }
                },
                "weight": 1.2
            }, {
                "filter": {
                    "match": {
                        "resource_label": "reuters"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "securelist"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "securityaffairs"
                    }
                },
                "weight": 0.8
            }, {
                "filter": {
                    "match": {
                        "resource_label": "securityintelligence"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "securityweek"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "techcrunch"
                    }
                },
                "weight": 1.2
            }, {
                "filter": {
                    "match": {
                        "resource_label": "thehackernews"
                    }
                },
                "weight": 1
            }, {
                "filter": {
                    "match": {
                        "resource_label": "threatpost"
                    }
                },
                "weight": 1.6
            }, {
                "filter": {
                    "match": {
                        "resource_label": "trendmicro"
                    }
                },
                "weight": 1.4
            }, {
                "filter": {
                    "match": {
                        "resource_label": "wired"
                    }
                },
                "weight": 1.2
            });
            json.query.bool.must[0].query_string.default_field ="*.processed";
        }         
        if(criteria.time_decay==true)
        {
            json.query.bool.must[1].function_score.functions.push({
                "exp": {
                    "published": {
                        "origin": "now",
                        "scale": "7d",
                        "offset": "7d",
                        "decay": 0.5
                             }
                             }
                    });
            json.query.bool.must[0].query_string.default_field ="*.processed";
        }

       
        console.log( JSON.stringify(json.query.bool.must[1].function_score.functions));

        json.query.bool.must[0].query_string.query=criteria.keyword; 

        console.log(json.query.bool.must[0].query_string.default_field);
        console.log("Keyword changed to ");
        console.log(json.query.bool.must[0].query_string.query);

        // console.log(json.query.bool.must[0].query_string.query = "hello"); 
        return json;
    }
}
