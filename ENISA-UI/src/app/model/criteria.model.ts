import { QueryFilter } from './../data/request';
import { WeightFunction } from "./../data/weight-function";
export interface ICriteria {
    index?: string;
    k_graph?: Boolean;
    time_decay?: Boolean;
    p_resources?: Boolean;
    knowledgeGraphDisabled: Boolean;
    timeDecayDisabled: Boolean;
    popularitySourcesDisabled: Boolean;
    news_articles?: Boolean;
    tweeter_feed?: Boolean;
    enisa_reports?: Boolean;
    enisa_recomend?: Boolean;
    date_range?: string;
    keyword?: string;
    url?: string;
    popularities? :any

    setPopularities(popularities : any)
}

export class Criteria implements ICriteria {
    index?: string = "content";
    k_graph?: Boolean = true;
    time_decay?: Boolean = false;
    p_resources?: Boolean = false;
    knowledgeGraphDisabled: Boolean = false;
    timeDecayDisabled: Boolean = false;
    popularitySourcesDisabled: Boolean = false;
    news_articles?: Boolean = true;
    tweeter_feed?: Boolean;
    enisa_reports?: Boolean;
    enisa_recomend?: Boolean;
    date_range?: string;
    keyword?: string;
    url?: string;
    popularities? : any

    constructor(params?: ICriteria) {
        if (params) {
            this.k_graph = params.k_graph;
            this.time_decay = params.time_decay;
            this.p_resources = params.p_resources;
            this.news_articles = params.news_articles;
            this.tweeter_feed = params.tweeter_feed;
            this.enisa_reports = params.enisa_reports;
            this.enisa_recomend = params.enisa_recomend;
            this.keyword = params.keyword;
            this.date_range = params.date_range;
            this.index = params.index;
            this.url = params.url;
        }
    }

    setPopularities(popularities) {
        this.popularities = popularities
    }

    build() {
        let queryFilter = QueryFilter()
        let query : any[] = queryFilter.query.bool.must
        let queryString = { "query_string": { "query": "", "analyze_wildcard": true, "default_field": "*" } }
        let functions = []
        
        let field = "*"
        if( this.index === "content" || this.index === "twitter" ) {
            field = this.k_graph ? "*.knowledge_graph" : "*.processed"
            let dateField = this.index === "twitter" ? "created_at" : "published";
            if ( this.time_decay ) {
                let expFunction = {}
                let params = { "origin": "now", "scale": "7d", "offset": "7d", "decay": 0.5 };
                expFunction[dateField] = params
                functions.push( { "exp": expFunction } );
            }
            if ( this.p_resources ) {
                let weightField = this.index === "twitter" ? "user.name" : "resource_label";
                let list = []
                for( let key in this.popularities ) {
                    let weight = WeightFunction()
                    weight["filter"]["match"][weightField] = key
                    weight["weight"] = this.popularities[key]
                    list.push(weight)
                }
                functions = functions.concat( list )
            }
            if( this.time_decay || this.p_resources ) {
                let functionScore = { "function_score": { "functions": functions } }
                query.push( functionScore )
            }
            if( this.date_range !== undefined && this.date_range !== "" ) {
                let dateRange = { "range": {} }
                let dates: string[] = this.date_range.toString().split(",", 2);
                let dateFrom = new Date(dates[0]).getTime();
                let dateTo = new Date(dates[1]).getTime();
                dateRange["range"][dateField] = { "gte": dateFrom, "lte": dateTo, "format": "epoch_millis" }
                query.push(dateRange)
            }
        }
        else if( this.index === "pdf_documents_light" ) {
            field = "summary"
        }
        else if ( this.index === "pdf_documents_light_recommendations" ) {
            field = "recommendations"
        }
        queryString["query_string"]["default_field"] = field
        queryString["query_string"]["query"] = this.keyword
        query.push(queryString)
        return queryFilter
    }
}
