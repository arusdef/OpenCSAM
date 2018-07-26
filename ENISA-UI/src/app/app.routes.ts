import { SearchHomeComponent } from './search-home/search-home.component';
import { ArticleSearchComponent } from './article-search/article-search.component';

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [{
    path: '',
   component: SearchHomeComponent,
  },
  {
    path: 'articleSearch',
    component: ArticleSearchComponent,
  }
];

export const appRoutes: any = RouterModule.forRoot(routes);
