import { Globals } from './../app/globals';
import { Observable } from 'rxjs/Rx';
import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpInterceptorService } from '@covalent/http';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable()
export class AppConfigService{
    public appData :string; 
    constructor(private _http: HttpInterceptorService,
        private _global:Globals, 
        private _snackBarService: MatSnackBar){

    }

    getAPI():any{

        const promise = this._http.get('./../../assets/data.json').map(result => result.json()).toPromise();
        promise.then(appConfig => { 
            this.appData = appConfig;
            this._global.setContentIndexURL(this.appData['ELASTIC_SEARCH_CONTENT_INDEX']);
            this._global.setUserName(this.appData['USER_NAME']);
            this._global.setPassword(this.appData['PASSWORD']);
         });
        return promise;
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