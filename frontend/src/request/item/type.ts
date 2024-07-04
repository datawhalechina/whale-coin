export interface IGetItemDetal{
    itemid:number
}

export interface IAddItem {
    name:string
    describe:string
    stock:number
    prince:number
    files:File[]
}

export interface IDeleteItem {
    itemid: number
}
export interface IAddOrder {
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

export  interface IGetAudtOrder{
    status:string
}

export interface IGetOrderDetal{
    orderid:number
}
export interface IDeleteOrder{
    orderid:number
}