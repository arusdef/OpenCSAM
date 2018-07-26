import { Globals } from './../globals';
import { Component, OnInit } from '@angular/core';
import { SearchService } from './../../services/search.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-search-home',
  templateUrl: './search-home.component.html',
  styleUrls: ['./search-home.component.scss']
})
export class SearchHomeComponent implements OnInit {
  //@ViewChild(SearchControlComponent) searchControl : SearchControlComponent;
  
 constructor(  private _searchService: SearchService,  
  private _router: Router,
  private _route: ActivatedRoute,
  private _global:Globals) { }

  ngOnInit() {
    
  }

  search(inputText:string) {
    this._global.setSearchInput(inputText);
    this._router.navigate(['/articleSearch']);
} 
}


