export interface IShards{
    total?:string;
    successful?:string;
    skipped?:string;
    failed?:string;
}

export class Shards implements IShards {
    total?:string;
    successful?:string;
    skipped?:string;
    failed?:string;

    constructor(params?: IShards) {
        if (params) {
            this.total=params.total;
            this.successful=params.successful;
            this.skipped=params.skipped;
            this.failed=params.failed;
        }
    }
}
