import { Injectable } from '@angular/core';
import { RequestOptionsArgs, Headers } from '@angular/http';
import { IHttpInterceptor } from '@covalent/http';

@Injectable()
export class RequestInterceptor implements IHttpInterceptor {
  // onRequest(requestOptions: RequestOptionsArgs): RequestOptionsArgs {
  //   // you add headers or do something before a request here.

  //   let headers: Headers = requestOptions.headers;
  //   if (!headers) {
  //     headers = new Headers();
  //   }

  //   debugger;
  //   // headers.append('Authorization', 'Basic ' +
  //   //   btoa('guest:teradata')); 
  //   //   headers.append('Content-Type','application/json');
     
  //   // requestOptions.headers = headers;
  //   // console.log("headers " + requestOptions.headers );
  //   // return requestOptions;
  // }
}