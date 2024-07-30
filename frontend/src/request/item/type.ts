export interface IGetItemDetal {
    itemid: number
}

export interface IAddItem {
    name: any
    describe: any
    stock: any
    prince: any
    // files: File[]
}

export interface IDeleteItem {
    itemid: number
}
export interface IAddOrder {
    user_id: number,
    itemid: number,
    quantity: number
    order_type: string
    status: string
    toal_price: number
    address: string
    phone: string
}
export interface IAuduitOrder {
    orderid: number
    status: string
}

export interface IGetAudtOrder {
    status: string
}

export interface IGetOrderDetal {
    orderid: number
}
export interface IDeleteOrder {
    orderid: number
}