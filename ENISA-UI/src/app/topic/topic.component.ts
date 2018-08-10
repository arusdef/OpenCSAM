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
  constructor() { console.log("Topic Component Creates"); }
  data: any[] = [];
  ngOnInit() {
    console.log("Topic Component Creates");
  
  }
  ngOnDestroy(){

  }
 
  
  search(newvalue:string){
    this.criteriaChange.emit(this.result.criteria);
  }
  

}
