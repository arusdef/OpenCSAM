export interface ISource {
    title?:string;
    link ?:string;
    content ?:string;
    published?:string;
    resource_type?:string;
    resource_label?:string;
}
export class Source implements ISource{
    title?:string;
    link ?:string;
    content ?:string;
    published?:string;
    resource_type?:string;
    resource_label?:string;

    constructor(params?:ISource){
        this.title=params.title;
        this.link=params.link;
        this.content=params.content;
        this.published=params.published;
        this.resource_type=params.resource_type;
        this.resource_label = params.resource_label;
    
    }
}