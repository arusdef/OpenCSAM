export interface ISource {
  title?: string;
  link?: string;
  content?: string;
  full_text?: string;
  summary?:string;
  recommendations?:string;
  published?: string;
  resource_type?: string;
  resource_label?: string;
  up_vote?: boolean;
  down_vote?: boolean;
  created_at?: string;
  //twitter
  id_str?: string;
  twitterUsername?: string;

}
export class Source implements ISource {
  title?: string;
  link?: string;
  content?: string;
  full_text?: string;
  summary?: string;
  recommendations?:string;
  published?: string;
  resource_type?: string;
  resource_label?: string;
  up_vote?: boolean = false;
  down_vote?: boolean = false;
  created_at?: string;
  id_str?: string = "";
  twitterUsername?: string;

  constructor(params?: ISource) {
    this.title = params.title;
    this.link = params.link;
    this.content = params.content;
    this.summary = params.summary;
    this.recommendations = params.recommendations;
    this.published = params.published;
    this.resource_type = params.resource_type;
    this.resource_label = params.resource_label;
    this.full_text = params.full_text;
    this.up_vote = false;
    this.down_vote = false;
    this.created_at = params.created_at;
    this.id_str = params.id_str;
    if(params["user"]) {
      this.twitterUsername = params["user"]["screen_name"]
    }
  }
}
