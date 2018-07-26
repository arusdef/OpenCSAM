import {Source} from './source.model';

export interface IHitsObjs { 

_index?: string;
_type?: string;
_id?: string;
_score?: number;
_source?: Source;

}

export class HitsObjs implements IHitsObjs{

_index?: string;
_type?: string;
_id?: string;
_score?: number;
_source?: Source;

    constructor(params?: IHitsObjs) {
        if (params) {
            this._index = params._index;
            this._type = params._type;
            this._id = params._id;
            this._score = params._score;
            this._source = new Source(params._source);
                console.log("score is" + params._score);
        }
}
}