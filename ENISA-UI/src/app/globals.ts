import { Criteria } from './model/criteria.model';
import { Injectable } from '@angular/core';

@Injectable() 
export class Globals {
    searchInput: string = '';
    
    setSearchInput(searchInput:string ){
      this.searchInput=searchInput;
    }
    getSearchInput(){
        return this.searchInput;
    }

    public findInArrayByName(arrayObject: Array<any>, name: string): any {

      if (arrayObject == null || arrayObject.length <= 0) {
  
        return null;
  
      }
     
      return arrayObject.find(
        x =>
         
         x['topic'] === name
         );
  
    }


  //   public checkForProperty(sourceCriteria:Criteria,newCriteria:Criteria): any {
  //     debugger;
  //     if(sourceCriteria.k_graph === newCriteria.k_graph || ){
  //       return true;
  //     }
  //     else {
  //     return false;
  //     }
  // }
  
}