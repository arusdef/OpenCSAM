import { Component, OnInit, Input } from '@angular/core';
import { ResponseTemplate } from '../model/responseTemplate.model';
import { saveAs } from 'file-saver/FileSaver';

@Component({
  selector: 'app-report-editor',
  templateUrl: './report-editor.component.html',
  styleUrls: ['./report-editor.component.scss']
})
export class ReportEditorComponent implements OnInit {

  @Input() result : ResponseTemplate;
  @Input() notes : {"note":string};

  constructor() { }

  ngOnInit() {
  }

  saveNotesAsFile(): void {
    let blob: Blob = new Blob([this.notes.note], { type: 'text/plain' });
    let filename: string = "notes."+(new Date()).toISOString()+".txt";
    saveAs(blob, filename);
  }

}
