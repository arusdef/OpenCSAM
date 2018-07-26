import {HitsObjs} from './hits-obj.model';
export interface IHits { 
    hitsObjs?: HitsObjs[];
}
export class Hits implements IHits {
   
    hitsObjs?: HitsObjs[]=[];

    constructor(params?: IHits) {
        if (params) {
            var index=0;
            while(index<params['hits'].length){
            this.hitsObjs.push(new HitsObjs(params['hits'][index]));
                index++;    
            }
        }

    }


}