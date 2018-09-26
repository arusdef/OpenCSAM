export interface ISourcePopularity {
  _initial: any;
  _current: any;

  getPopularitiesFilter(): any
  update(source: string, value: number)
}

export class SourcePopularity implements ISourcePopularity {
  _initial: any;
  _current: any;
  constructor(current: any) {
    this._current = current;
    this._initial = {
      arstechnica: 1.6,
      bankinfosecurity: 1.2,
      bleepingcomputer: 1,
      csoonline: 1.4,
      darkreading: 1.4,
      euractiv: 1.4,
      itsecurityguru: 0.8,
      malwarebytes: 1.6,
      nakedsecurity: 1,
      politico: 1.2,
      reuters: 1.4,
      securelist: 1.4,
      securityaffairs: 0.8,
      securityintelligence: 1.4,
      securityweek: 1.4,
      techcrunch: 1.2,
      thehackernews: 1,
      threatpost: 1.6,
      trendmicro: 1.4,
      wired: 1.2
    };
  }

  getPopularitiesFilter(): any {
    return {...this._initial, ...this._current}
  }

  update(sourceName: string, value: number) {
    if ( this._current[sourceName] ) {
      this._current[sourceName] += value
    }
    else if( this._initial[sourceName] ) {
      this._current[sourceName] = this._initial[sourceName] + value
    }
    else {
      this._current[sourceName] = value
    }
  }
}
