import { Component, OnInit,Input } from '@angular/core';
import { ITdDataTableColumn } from '@covalent/core/data-table';

@Component({
  selector: 'app-result-template',
  templateUrl: './result-template.component.html',
  styleUrls: ['./result-template.component.scss']
})
export class ResultTemplateComponent implements OnInit {
  @Input() result: any[];

  columns: ITdDataTableColumn[] = [
    { name: 'result',  label: 'result' }
  ];
  constructor() { }
  ngOnInit() {
  
    }
  }

