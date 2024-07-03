
type Item={
    id:number
    name:string
    describe:string
    stock:number
    create_time:Date
    prince:number
    create_user:number
    img_path:string
}
type Order={
    id:number
    user_id:number
    itemid:number
    quantity:number
    order_type:string
    status:string
    toal_price:number
    address:string
    phone:string
    create_time:Date
    audit_id:number
}

export interface IGetItemDetal{
    itemid:number
}

export interface IAddItem {
    item:Item
    files:File[]
}

export interface IDeleteItem {
    itemid: number
}
export interface IAddOrder {
    order:Order
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