export interface IAddItem {
    name:string
    describe:string
    stock:number
    prince:number
}

export interface IaddOrder {
    itemid:number
    quantity:number
    order_type:string
    status:string
    toal_price:number
    address:string
    phone:string
}

export interface IAuduitOrder {
    orderid: number
    status: string
}

export interface IGetAudtOrder {
    statusId:string
}