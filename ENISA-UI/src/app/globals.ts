import { Criteria } from './model/criteria.model';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import {Observable} from 'rxjs';

@Injectable() 
export class Globals {
    searchInput: string = '';
    dateRange :string ='';
    private tabDataStatus = new BehaviorSubject<string>("");
    contentIndexURL :string ='';
  userName: string = '';
  password: string = '';

    setSearchInput(searchInput:string ){
      this.searchInput=searchInput;
    }
    getSearchInput(){
        return this.searchInput;
    }

    setContentIndexURL(contentIndexURL:string ){
      this.contentIndexURL=contentIndexURL;
    }
    getContentIndexURL(){
        return this.contentIndexURL;
    }

    setDateRange(dateRange:string ){
      this.dateRange=dateRange;
    }
    getDateRange(){
        return this.dateRange;
    }

    
    setTabDataStatus(value: string) {
      this.tabDataStatus.next(value);
      }

  getTabDataStatus(): Observable<string> {
    return this.tabDataStatus.asObservable();
  }

  setUserName(userName: string) {
    this.userName = userName;
  }

  getUserName() {
    return this.userName;
  }
  setPassword(password: string) {
    this.password = password;
  }

  gePassword() {
    return this.password;
  }
}