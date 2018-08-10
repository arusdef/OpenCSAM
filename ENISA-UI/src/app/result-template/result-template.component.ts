  import { Component, OnInit,Input } from '@angular/core';
import { ITdDataTableColumn,TdDataTableService,TdDataTableSortingOrder } from '@covalent/core/data-table';
import { IPageChangeEvent } from '@covalent/core/paging';
import {ResponseTemplate} from './../model/responseTemplate.model';
import { Globals } from '../globals';
@Component({
  selector: 'app-result-template',
  templateUrl: './result-template.component.html',
  styleUrls: ['./result-template.component.scss']
})
export class ResultTemplateComponent implements OnInit {
  @Input() result: ResponseTemplate;
  
  pageSize: number = 10;
  filteredTotal :number =0;
  fromRow: number = 1;
  currentPage: number = 1;
  searchTerm: string = '';
  sortBy: string = '';
  sortOrder: TdDataTableSortingOrder = TdDataTableSortingOrder.Descending;
  filteredData: any[] = [];

  columns: ITdDataTableColumn[] = [
    { name: 'result',  label: 'result' }
  ];
  constructor(private _dataTableService: TdDataTableService,private _global:Globals) { }
  ngOnInit() {
 // this.filteredTotal  = this.result[0].hits.hitsObjs!= undefined ? this.result[0].hits.hitsObjs.length :50;
 this._global.getTabDataStatus().subscribe(status => 
  { 
    if(this.result.topic==status)
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
      let newData: any[] = this.result.hits.hitsObjs;
      let excludedColumns: string[] = this.columns
      .filter((column: ITdDataTableColumn) => {
        return ((column.filter === undefined && column.hidden === true) ||
                (column.filter !== undefined && column.filter === false));
      }).map((column: ITdDataTableColumn) => {
        return column.name;
      });
   //   newData = this._dataTableService.filterData(newData, this.searchTerm, true, excludedColumns);
      this.filteredTotal = newData.length;
   //   newData = this._dataTableService.sortData(newData, this.sortBy, this.sortOrder);
     newData = this._dataTableService.pageData(newData, this.fromRow, this.currentPage * this.pageSize);
      this.filteredData = newData;
    }

  }

