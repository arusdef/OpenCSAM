import { ResponseTemplate } from "./../model/responseTemplate.model";
import { Component, OnInit } from "@angular/core";
import { Globals } from "./../globals";
import { SearchService } from "./../../services/search.service";
import { Template } from "./../model/template.model";
import { MatTabChangeEvent } from "@angular/material/tabs";
import { Criteria } from "./../model/criteria.model";
import { Router, ActivatedRoute } from "@angular/router";

@Component({
  selector: "app-article-search",
  templateUrl: "./article-search.component.html",
  styleUrls: ["./article-search.component.scss"]
})
export class ArticleSearchComponent implements OnInit {
  response: Template = new Template();
  topics: string[] = ["Custom", "Threats", "Technology", "Business", "Policy", "Geopolitics"];
  view: "search" | "report" = "search";
  notes: { note: string } = { note: "" };
  currentTab = "Custom";

  constructor( private _searchService: SearchService, private _router: Router, 
    private _route: ActivatedRoute, private _global: Globals ) {
    for (const index in this.topics) {
      let responseTemplate = new ResponseTemplate()
      responseTemplate.topic = this.topics[index];
      this.response.topics.push(responseTemplate);
    }
  }

  ngOnInit() {
    let criteria = new Criteria()
    criteria.keyword = this._global.getSearchInput()
    criteria.date_range = this._global.getDateRange()
    criteria.index = "content"
    this._searchService.getResults(criteria).then(result => {
      let custom = this.response.topics[0]
      custom.setSearchResult(result);
      custom.isInitialized = true;
      custom.criteria = criteria
      this.currentTab = custom.topic;
      this._global.setTabDataStatus(this.currentTab);
    });
    this._searchService.loadSourcePopularity();
  }

  tabChanged(tabChangeEvent: MatTabChangeEvent) {
    this.currentTab = tabChangeEvent.tab.textLabel.toString();
    let topicIndex = this.topics.findIndex(element => {
      return element == this.currentTab;
    });
    let currentTopic = this.response.topics[topicIndex];
    if (currentTopic.topic != "Custom") {
      currentTopic.criteria.keyword = currentTopic.topic;
    }
    if (!currentTopic.isInitialized) {
      currentTopic.isInitialized = true;
      this._searchService.getResults(currentTopic.criteria).then(result => {
        this.response.topics[topicIndex].criteria.date_range = this._global.getDateRange();
        this.response.topics[topicIndex].setSearchResult(result);
        this._global.setTabDataStatus(this.currentTab);
      });
    }
  }

  setView(view: "search" | "report"): void {
    this.view = view;
  }

  loadData() {}

  criteriaChange(criteria: Criteria) {
    let topicIndex = this.topics.findIndex(element => {
      return element == this.currentTab;
    });
    let template = this.response.topics[topicIndex]
    criteria.setPopularities(this._global.getSourcePopularity().getPopularitiesFilter())
    this._searchService.getResults(criteria).then(result => {
      template.criteria.date_range = this._global.getDateRange();
      template.setSearchResult(result);
      this._global.setTabDataStatus(this.currentTab);
    });
  }

  navigate() {
    this._router.navigate(["/"]);
  }

  vote(data) {
    this._searchService.updateSourcePopularity(data);
  }
}
