import { ResponseTemplate } from './../model/responseTemplate.model';
import { Component, OnInit } from '@angular/core';
import { Globals } from './../globals';
import { SearchService } from './../../services/search.service';
import { Template } from './../model/template.model';
import { MatTabChangeEvent } from '@angular/material/tabs';
import {Criteria} from './../model/criteria.model';
import {Router, ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-article-search',
  templateUrl: './article-search.component.html',
  styleUrls: ['./article-search.component.scss']
})
export class ArticleSearchComponent implements OnInit {
  response: Template = new Template();
  topics: string[] = ['Custom', 'Threats', 'Technology', 'Business', 'Policy', 'Geopolitics'];
  view: "search"|"report" = "search";
  notes: {"note":string} = { "note":""};
  currentTab ='Custom';
 
  constructor(private _searchService: SearchService,   private _router: Router, private _route:ActivatedRoute, 
    private _global: Globals) {
      for (const index in this.topics) {
        this.response.topics.push(new ResponseTemplate());
        this.response.topics[index].topic = this.topics[index];
      }
    }

  ngOnInit() {


  let data = this._searchService.getResults(this._global.getSearchInput()).then(
      result => {
        this.response.topics[0].setElasticSearchResult(result);
        this.response.topics[0].isInitialized = true;
        console.log("criteria object");
        console.log( this.response.topics[0].criteria);
        this.response.topics[0].criteria.keyword=this._global.getSearchInput();
        console.log("setting date range to " + this._global.getDateRange()); 
        this.response.topics[0].criteria.date_range = this._global.getDateRange();
        this.currentTab=  this.response.topics[0].topic;
        this._global.setTabDataStatus(this.currentTab);

      }
    );
  }
  tabChanged(tabChangeEvent: MatTabChangeEvent) {

    this.currentTab = tabChangeEvent.tab.textLabel.toString();
    let topicIndex = this.topics.findIndex(element => {return element == this.currentTab});
    let currentTopic = this.response.topics[topicIndex];    
    if(currentTopic.topic!='Custom')
      currentTopic.criteria.keyword=currentTopic.topic;
    if (!currentTopic.isInitialized) {
      currentTopic.isInitialized = true;
      let data = this._searchService.getResults(this.currentTab).then(
        result => {
          console.log("result from service");
          console.log(result);
          this.response.topics[topicIndex].criteria.date_range = this._global.getDateRange();
          this.response.topics[topicIndex].setElasticSearchResult(result);
          this._global.setTabDataStatus(this.currentTab);
          console.log("After setting model, result from model, aftwer switching tab");
          console.log(this.response);

        }
      );
    }


  }

  setView(view:"search"|"report"): void{
    console.log("inside set view");
    this.view = view;
  }

  loadData(){

  }
 


  criteriaChange(criteria:Criteria){
    console.log("criteria change , current tab is "+ this.currentTab);
    console.log(criteria);
    let topicIndex = this.topics.findIndex(element => {return element == this.currentTab});
    //this.response.topics[topicIndex].criteria.setCriteria(criteria);

    let data = this._searchService.getResults(this.currentTab,criteria).then(
      result => {
        console.log("result from service");
        console.log(result);
        this.response.topics[topicIndex].criteria.date_range = this._global.getDateRange();
        this.response.topics[topicIndex].setElasticSearchResult(result);
        this._global.setTabDataStatus(this.currentTab);
        console.log("After setting model, result from model, aftwer switching tab");
        console.log(this.response);

      }
    );

  }
  navigate(){
    this._router.navigate(['/']);
  }
}
