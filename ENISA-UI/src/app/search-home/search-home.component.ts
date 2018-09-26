import { Globals } from "./../globals";
import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { SearchService } from "./../../services/search.service";
@Component({
  selector: "app-search-home",
  templateUrl: "./search-home.component.html",
  styleUrls: ["./search-home.component.scss"]
})
export class SearchHomeComponent implements OnInit {
  dateRange: string;
  constructor(
    private _router: Router,
    private _route: ActivatedRoute,
    public _global: Globals,
    private _searchService: SearchService
  ) {}

  ngOnInit() {
    this.dateRange = this._global.getDateRange();
  }

  search(inputText: string) {
    this._global.setDateRange(this.dateRange);
    this._global.setSearchInput(inputText);
    this._router.navigate(["/articleSearch"]);
  }
}
