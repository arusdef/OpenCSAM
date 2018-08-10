import { Globals } from './../app/globals';
import { Criteria } from './../app/model/criteria.model';

import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpInterceptorService } from '@covalent/http';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { HttpRequest } from 'selenium-webdriver/http';
import { request_json } from './../app/data/request';
import { Http, Headers, RequestOptions } from '@angular/http';
import { MatSnackBar } from '@angular/material/snack-bar';


@Injectable()
export class SearchService {

  headers: HttpHeaders = new HttpHeaders();
  tab_name: string = '';
  createAuthorizationHeader(headers: HttpHeaders) {
    headers = new HttpHeaders();
    headers.set('Authorization', 'Basic ' +
      btoa('guest:teradata'));
  }
  loaded: boolean=false;

  constructor(private _http: HttpInterceptorService,
    private _global: Globals,   private _snackBarService: MatSnackBar) {
     }
  getResults(keyword: string, criteria?: Criteria): any {

  //  let actionUrl = 'https://elastic.opencsam.enisa.europa.eu/content/_search';
    // if(this.loaded){
   let actionUrl = this._global.getContentIndexURL();
      let headers = new Headers({ 'Content-Type': 'application/json' });
      headers.append("Authorization", "Basic " + btoa('guest' + ":" + 'teradata'));

      let options = new RequestOptions({ headers: headers });
     // debugger;

      let jsonData;
      if (criteria) {
        jsonData = criteria.setCriteria(criteria);
        console.log("JSON Data to Send: " + JSON.stringify(jsonData));
        console.log("Action URL: " + actionUrl);

      }
      else {
        let cri: Criteria = new Criteria();
        cri.keyword = keyword;
        cri.date_range = this._global.getDateRange();
        jsonData = cri.setCriteria(cri);
        console.log("JSON Data to Send: " + JSON.stringify(jsonData));
        console.log("Action URL: " + actionUrl);

      }

      return this._http.post(actionUrl, JSON.stringify(jsonData), options)
        .toPromise()
        .then(this.extractData)
      //  .catch(this.handleError);
        .catch((err)=>{this.handleError(err);});
    
  }
  private extractData(res: Response) {

    let body = res.json();
    // debugger;
    console.log("Service.getEnisa() Response: ");
    console.log(body);

    return body || {};

  }

  private handleError(error: any): Promise<any> {

    console.error("Error at Service.GetEnisa(): " + error);
    this._snackBarService.open("Error while accessing database, error : " + error , "OK");
    return Promise.reject(error.message || error);
  }

 
}
