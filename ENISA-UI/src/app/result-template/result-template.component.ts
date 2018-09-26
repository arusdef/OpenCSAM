import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ITdDataTableColumn, TdDataTableService, TdDataTableSortingOrder } from '@covalent/core/data-table';
import { IPageChangeEvent } from '@covalent/core/paging';
import { ResponseTemplate } from './../model/responseTemplate.model';
import { Globals } from '../globals';
import { IHitsObjs } from '../model/hits-obj.model';
@Component({
  selector: 'app-result-template',
  templateUrl: './result-template.component.html',
  styleUrls: ['./result-template.component.scss']
})
export class ResultTemplateComponent implements OnInit {
  @Input() result: ResponseTemplate;
  @Output() idEvent = new EventEmitter<any>();

  pageSize: number = 20;
  filteredTotal: number = 0;
  fromRow: number = 1;
  currentPage: number = 1;
  searchTerm: string = '';
  sortBy: string = '';
  sortOrder: TdDataTableSortingOrder = TdDataTableSortingOrder.Descending;
  filteredData: any[] = [];
 
  columns: ITdDataTableColumn[] = [
    { name: 'result', label: 'result' }
  ];
  constructor(private _dataTableService: TdDataTableService, private _global: Globals) { }
  ngOnInit() {
    this._global.getTabDataStatus().subscribe(status => {
      if (this.result.topic == status)
        this.filter();
    });
  }

  page(pagingEvent: IPageChangeEvent): void {
    this.fromRow = pagingEvent.fromRow;
    this.currentPage = pagingEvent.page;
    this.pageSize = pagingEvent.pageSize;
    this.filter();
  }

  filter(): void {
    if(this.result.hits!== null) {
      let newData: any[] = this.result.hits.hitsObjs;
      this.columns.filter((column: ITdDataTableColumn) => {
        return ((column.filter === undefined && column.hidden === true) || 
          (column.filter !== undefined && column.filter === false));
      }).map((column: ITdDataTableColumn) => {
        return column.name;
      });
      this.filteredTotal = this.result.hits.hitsObjs.length;
      newData = this._dataTableService.pageData(newData, this.fromRow, this.currentPage * this.pageSize);
      this.filteredData = newData;
    }
  }

  toggleUpVote(article : IHitsObjs) {
    let articleSource = article._source
    articleSource.up_vote = !articleSource.up_vote;
    var source = "";
    if ( articleSource.resource_label ) {
      source = articleSource.resource_label
    }
    else if( articleSource.twitterUsername ) {
      source = articleSource.twitterUsername
    }
    source = source.replace(/ /g, "").trim().toLocaleLowerCase()
    let value = 0.5
    this._global.getSourcePopularity().update(source, value)
    let docInfo = {};
    docInfo['value'] = value
    docInfo['source'] = source
    this.idEvent.emit(JSON.stringify(docInfo))
  }

  toggleDownVote(article : IHitsObjs) {
    let articleSource = article._source
    articleSource.down_vote = !articleSource.down_vote;
    var source = "";
    if ( articleSource.resource_label ) {
      source = articleSource.resource_label.toLocaleLowerCase()
    }
    else if( articleSource.twitterUsername ) {
      source = articleSource.twitterUsername.toLocaleLowerCase()
    }
    source = source.replace(/ /g, "").trim().toLocaleLowerCase()
    let value = -0.5
    this._global.getSourcePopularity().update(source, value)
    let docInfo = {};
    docInfo['value'] = value
    docInfo['source'] = source
    this.idEvent.emit(JSON.stringify(docInfo));
  }
}

