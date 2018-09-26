import { Globals } from '../app/globals';
import { NgModule, Type,APP_INITIALIZER } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatRadioModule} from '@angular/material/radio';

import { HttpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { CovalentPagingModule } from '@covalent/core/paging';
import { BrowserModule, Title }  from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CovalentSearchModule } from '@covalent/core/search';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatInputModule } from '@angular/material/input';
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatTabsModule} from '@angular/material/tabs';
import { CovalentCommonModule } from '@covalent/core/common';
import { CovalentLayoutModule } from '@covalent/core/layout';
import { CovalentDataTableModule } from '../../node_modules/@covalent/core/data-table';
import {MatSelectModule} from '@angular/material/select';

import { CovalentMediaModule } from '@covalent/core/media';
import { CovalentLoadingModule } from '@covalent/core/loading';

import { CovalentHttpModule, IHttpInterceptor } from '@covalent/http';

import { NgxChartsModule } from '@swimlane/ngx-charts';

import { appRoutes } from './app.routes';
import { CovalentVirtualScrollModule } from '@covalent/core/virtual-scroll';

import { AppComponent } from './app.component';
import { RequestInterceptor } from '../config/interceptors/request.interceptor';
import { MOCK_API } from '../config/api.config';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {SearchService} from '../services/search.service';
import { ArticleSearchComponent } from './article-search/article-search.component';
import { SearchHomeComponent } from './search-home/search-home.component';
import { EnisaFooterComponent } from './enisa-footer/enisa-footer.component';
import { ResultTemplateComponent } from './result-template/result-template.component';
import { TopicComponent } from './topic/topic.component';
import { ReportEditorComponent } from './report-editor/report-editor.component';
import { HashLocationStrategy, LocationStrategy } from '@angular/common';
import { AppConfigService } from '../services/load-config.service';

const httpInterceptorProviders: Type<any>[] = [
  RequestInterceptor,
];

export function getAPI(): string {
  return MOCK_API;
}
export function appConfigServiceFactory(provider: AppConfigService) {
  return () => provider.getAPI();
}

@NgModule({
  declarations: [
    AppComponent,
    ArticleSearchComponent,
    SearchHomeComponent,
    EnisaFooterComponent,
    ResultTemplateComponent,
    TopicComponent,
    ReportEditorComponent,
    
  ], // directives, components, and pipes owned by this NgModule
  imports: [
    // angular modules
    CovalentSearchModule,
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    MatRadioModule,
    FormsModule,
    HttpClientModule,
    HttpModule,
    CovalentVirtualScrollModule,
    // material modules
    MatButtonModule,
    MatSlideToggleModule,
    MatCardModule,
    MatIconModule,
    MatListModule,
    MatCheckboxModule,
    MatDividerModule,
    MatSnackBarModule,
    MatInputModule,
    MatTabsModule,
    MatToolbarModule,
    MatSelectModule,
    // covalent modules
    CovalentCommonModule,
    CovalentLayoutModule,
    CovalentMediaModule,
    CovalentLoadingModule,
    CovalentDataTableModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    CovalentPagingModule,
    CovalentHttpModule.forRoot({
      interceptors: [{
        interceptor: RequestInterceptor, paths: ['**'],
      }],
    }),
    // external modules
    NgxChartsModule,
    // routes
    appRoutes,
  ], // modules needed to run this modules
  providers: [  Globals,
    httpInterceptorProviders,SearchService,
    AppConfigService,
    { provide: APP_INITIALIZER, useFactory: appConfigServiceFactory, deps: [AppConfigService], multi: true },
    // {provide: LocationStrategy, useClass: HashLocationStrategy}, 
  ], // additional providers needed for this module
  entryComponents: [ ],
  bootstrap: [ AppComponent ],
})
export class AppModule {}
