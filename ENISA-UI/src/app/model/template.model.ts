    import {ResponseTemplate} from './responseTemplate.model';

export class Template {
    date_from?;string;
    date_to?:string;
    notes?:string; //to be decided for level
    topics :ResponseTemplate[] = [];

    constructor(params?:Template){
        if(params){
          
            this.date_from=params.date_from;
            this.date_to=params.date_to;
            this.notes=params.notes;//to be decided for level
            var index=0;
            while(index<params.topics.length){
                this.topics.push( new ResponseTemplate(params.topics[index]));
                index++;
            }
        }
    }
}