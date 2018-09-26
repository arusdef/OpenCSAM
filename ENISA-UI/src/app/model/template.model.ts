import { ResponseTemplate } from "./responseTemplate.model";

export class Template {
  notes?: string; //to be decided for level
  topics: ResponseTemplate[] = [];

  constructor(notes? : string, topics?: ResponseTemplate[]) {
      this.notes = notes
      this.topics = topics || []
  }
}
