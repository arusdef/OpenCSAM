import { Globals } from './../globals';
import { ResponseTemplate } from './../model/responseTemplate.model';
import { Component, OnInit, OnDestroy,Input,Output,EventEmitter   } from '@angular/core';
import {Criteria} from './../model/criteria.model';
@Component({
  selector: 'app-topic',
  templateUrl: './topic.component.html',
  styleUrls: ['./topic.component.scss']
})
export class TopicComponent implements OnInit,OnDestroy {

  @Input() result : ResponseTemplate = new ResponseTemplate();
  @Output() criteriaChange : EventEmitter<Criteria> = new EventEmitter();
  @Output() idChange = new EventEmitter();

  selectedIndex: string;
  data: any[] = [];
 
  indices = [
    { name: 'content', label: 'News Articles' },
    { name: 'twitter', label: 'Twitter Feed' },
    { name: 'pdf_documents_light', label: 'ENISA Reports' },
    { name: 'pdf_documents_light_recommendations', label: 'ENISA Recommendations' },
  ];

  constructor() {
  }
  
  ngOnInit() {
    this.selectedIndex='content';
  }

  ngOnDestroy(){
  }

  search() {
    this.criteriaChange.emit(this.result.criteria);
  }
  
  idReceive(id:string) {
    this.idChange.emit( '[' + id + ', '+ JSON.stringify(this.result.criteria) + ']');
  }

  updateDataTable(newValue) {
    let index = newValue.value
    let criteria = this.result.criteria
    criteria.index = index;
    criteria.knowledgeGraphDisabled = (index === 'pdf_documents_light' || index === 'pdf_documents_light_recommendations' )
    criteria.timeDecayDisabled = (index === 'pdf_documents_light' || index === 'pdf_documents_light_recommendations' )
    criteria.popularitySourcesDisabled = (index === 'pdf_documents_light' || index === 'pdf_documents_light_recommendations' )
  }
}
