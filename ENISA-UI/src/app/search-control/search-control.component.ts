import { Globals } from './../globals';
import { Component, OnInit,Input } from '@angular/core';
import { SearchService } from './../../services/search.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-search-control',
  templateUrl: './search-control.component.html',
  styleUrls: ['./search-control.component.scss']
})
export class SearchControlComponent implements OnInit {

  searchInputTerm:string;

  constructor(
    private _searchService: SearchService,  
    private _router: Router,
    private _route: ActivatedRoute,
    private _global:Globals) { }

  ngOnInit() {
    this.searchInputTerm = this._global.getSearchInput();
  }
  @Input() searchInput :string;

  search(inputText:string) {
      this._global.setSearchInput(inputText);
      this._router.navigate(['/articleSearch']);
  }




}
