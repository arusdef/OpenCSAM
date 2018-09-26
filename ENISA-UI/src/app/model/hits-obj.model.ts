import { Highlight } from "./highlight.model";
import { Source } from "./source.model";

export interface IHitsObjs {
  _index?: string;
  _type?: string;
  _id?: string;
  _score?: number;
  _source?: Source;
  highlight?: Highlight;
}

export class HitsObjs implements IHitsObjs {
  _index?: string;
  _type?: string;
  _id?: string;
  _score?: number;
  _source?: Source;
  highlight?: Highlight;
  constructor(params?: IHitsObjs) {
    if (params) {
      this._index = params._index;
      this._type = params._type;
      this._id = params._id;
      this._score = params._score;
      this._source = new Source(params._source);
      this.highlight = params.highlight;
    }
  }

  getTitle(): string {
    return this._source.title;
  }

  getType(): string {
    return this._source.resource_type ? this._source.resource_type : this._type
  }

  getLink(): string {
    let link = this._source.link ? this._source.link : "https://twitter.com/statuses/" + this._source.id_str;
    return link;
  }

  getPublishedAt(): string {
    return this._source.published ? this._source.published : this._source.created_at
  }

  getSource(): string {
    var v = ""
    let source = this._source
    if (source.resource_label) {
      v = source.resource_label
    }
    else if (source.twitterUsername) {
      v = source.twitterUsername
    }
    else {
      v = "Internal"
    }
    return v
  }

  getContent(): string {
    var v = "";
    if (this._source.content && this._source.content !== "") {
      v = this._source.content
    }
    else if (this._source.full_text && this._source.full_text !== "") {
      v = this._source.full_text
    }
    else if (this._source.recommendations && this._source.recommendations !== "") {
      v = this._source.recommendations
    }
    else if (this._source.summary && this._source.summary !== "") {
      v = this._source.summary
    }
    for (var key in this.highlight) {
      if (key.startsWith("content") || key.startsWith("full_text")
        || key.startsWith("summary") || key.startsWith("recommendations")) {
        v = this.highlight[key][0];
      }
    }
    return v !== "" ? v.substr(0, 600) : v;
  }

  getFullContent(): string {
    var v = "";
    if (this._source.content && this._source.content !== "") {
      v = this._source.content
    }
    else if (this._source.full_text && this._source.full_text !== "") {
      v = this._source.full_text
    }
    else if (this._source.recommendations && this._source.recommendations !== "") {
      v = this._source.recommendations
    }
    else if (this._source.summary && this._source.summary !== "") {
      v = this._source.summary
    }
    return v;
  }

  showLink(): Boolean {
    return (this._index == 'content' || this._index == 'twitter')
   
  }
}
