import { vote } from "./../app/data/vote";
import { Globals } from "./../app/globals";
import { Criteria } from "./../app/model/criteria.model";

import { Injectable } from "@angular/core";
import { Response } from "@angular/http";
import { HttpInterceptorService } from "@covalent/http";
import { HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { map } from "rxjs/operators";
import { HttpRequest } from "selenium-webdriver/http";
import { Http, Headers, RequestOptions } from "@angular/http";
import { MatSnackBar } from "@angular/material/snack-bar";
import { SourcePopularity } from '../app/model/source-popularity'

@Injectable()
export class SearchService {
  tab_name: string = "";
  loaded: boolean = false;

  createHeaders() : Headers {
    let headers = new Headers({ "Content-Type": "application/json" });
    let username = this._global.userName
    let password = this._global.password
    headers.set("Authorization", "Basic " + btoa(username + ":" + password));
    return headers
  }

  constructor(private _http: HttpInterceptorService, 
    private _global: Globals,
    private _snackBarService: MatSnackBar) {
  }

  getResults(criteria?: Criteria): any {
    let actionUrl = this._global.getContentIndexURL();
    let options = new RequestOptions({ headers: this.createHeaders() });
    let jsonData = criteria.build();

    // FIXME improve this
    let index = (criteria.index === undefined ? "content" : criteria.index)
    if ( index === "pdf_documents_light_recommendations" ) {
      index = index.replace("_recommendations", "")
    }
    // /FIXME
    actionUrl = actionUrl + index + "/_search";
    return this._http.post(actionUrl, JSON.stringify(jsonData), options).toPromise()
      .then(this.extractData)
      .catch(err => {
        this.handleError(err);
      });
  }

  private extractData(res: Response) {
    let body = res.json();
    return body || {};
  }

  private handleError(error: any): Promise<any> {
    this._snackBarService.open("Error while accessing database, error : " + error, "OK");
    return Promise.reject(error.message || error);
  }

  updateSourcePopularity(sourcePopularity: any) {
    let data = JSON.parse(sourcePopularity)[0];
    let popularityFunction = vote();
    let source = data["source"];
    let scriptSource = "if ( ctx._source.#SOURCE == null ) { ctx._source.#SOURCE = 0.5 } else if ( ( ctx._source.#SOURCE + params.value ) > 0 ) { ctx._source.#SOURCE += params.value }";
    popularityFunction["script"]["source"] = scriptSource.replace(/#SOURCE/g, source);
    popularityFunction["script"]["params"]["value"] = data["value"];
    popularityFunction["upsert"][source] = data["value"];
    let actionUrl = this._global.contentIndexURL + "source_popularity/_doc/1/_update";
    let options = new RequestOptions({ headers: this.createHeaders() });
    return this._http.post(actionUrl, JSON.stringify(popularityFunction), options).toPromise()
      .then(this.extractData)
      .catch(err => {
        this.handleError(err);
      });
  }

  loadSourcePopularity() {
    let actionUrl = this._global.contentIndexURL + "source_popularity/_doc/1";
    let options = new RequestOptions({ headers: this.createHeaders() });
    let global : Globals = this._global
    return this._http.get(actionUrl, options).toPromise().then(function(response) {
      global.setSourcePopularity(new SourcePopularity(response.json()["_source"]))
    });
  }
}
