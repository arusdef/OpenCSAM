import { Criteria } from './../app/model/criteria.model';

import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpInterceptorService } from '@covalent/http';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { HttpRequest } from 'selenium-webdriver/http';
import {request_json} from './../app/data/request';
import { Http, Headers, RequestOptions } from '@angular/http';
@Injectable()
export class SearchService {

  headers: HttpHeaders = new HttpHeaders();
  tab_name:string='';
  createAuthorizationHeader(headers: HttpHeaders) {
    headers = new HttpHeaders();
    headers.set('Authorization', 'Basic ' +
      btoa('guest:teradata')); 
  }

     constructor(private _http: HttpInterceptorService){}
getResults(keyword:string,criteria?:Criteria): any {
  
  let actionUrl = 'https://elastic.opencsam.enisa.europa.eu/content/_search';

   let headers = new Headers({ 'Content-Type': 'application/json' });
   headers.append("Authorization", "Basic " + btoa('guest' + ":" + 'teradata'));

  let options = new RequestOptions({ headers: headers });
  debugger;
 
let jsonData;
if(criteria){
   jsonData = criteria.setCriteria(criteria);
  console.log("JSON Data to Send: " + JSON.stringify(jsonData));
  console.log("Action URL: " + actionUrl);

}
else 
{
 let cri:Criteria = new Criteria();
  cri.keyword=keyword;
  jsonData = cri.setCriteria(cri);
  console.log("JSON Data to Send: " + JSON.stringify(jsonData));
  console.log("Action URL: " + actionUrl);

}

  return this._http.post(actionUrl, JSON.stringify(jsonData), options)
    .toPromise()
    .then(this.extractData)
    .catch(this.handleError);


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

  return Promise.reject(error.message || error);
}
}
