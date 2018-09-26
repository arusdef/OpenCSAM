import { Criteria } from './criteria.model';
import { Hits } from './hits.model';
import { Shards } from './shards.model';
import { HitsObjs } from './hits-obj.model';
export interface IResponseTemplate{
    took?: string;
    timed_out?: string;
    _shards?: Shards;
    hits?:Hits;
    topic?:string;
    rpt?:string;
    criteria?:Criteria;
    isInitialized:Boolean; // Check for the first time
    selected:HitsObjs[]; // User selections from the articlesearch view
    query:string; // Search query term
}

export class ResponseTemplate implements IResponseTemplate {
    took?: string;
    timed_out?: string;
    _shards?: Shards;
    hits?:Hits= null;
    topic?:string;
    rpt?:string;
    criteria?:Criteria = new Criteria();
    isInitialized:Boolean = false;
    selected: HitsObjs[] = [];
    query: string = ""

    constructor(params?: IResponseTemplate) {
        if (params) {
            this.took = params.took;
            this.timed_out = params.timed_out;
            this._shards = new Shards(params._shards);
            this.topic = params.topic;
            this.rpt = params.rpt;
            this.criteria = params.criteria == null ? new Criteria() : new Criteria(params.criteria);
            this.hits = params.hits==null? new Hits():new Hits(params.hits);
            this.isInitialized = params.isInitialized;
            this.selected = params.selected;
            this.query = params.query;
        }
    }

    setSearchResult(params:any): void {
        this.took = params.took;
        this.timed_out = params.timed_out;
        this._shards = new Shards(params._shards);
        this.hits = params.hits == null ? new Hits() : new Hits(params.hits);
    }
}
