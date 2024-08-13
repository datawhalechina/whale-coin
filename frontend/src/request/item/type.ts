// 定义一个用于获取物品详情信息的接口，该接口包含一个必需的物品 ID 属性
export interface IGetItemDetal {
    itemid: number
}

// 定义一个用于添加物品的接口
export interface IAddItem {
    // 物品名称，可以是任何类型
    name: any
    // 物品描述，也可以是任何类型
    describe: any
    // 物品库存，数据类型不限
    stock: any
    // 物品价格，数据类型任意
    prince: any
    // files: File[]
}

// 定义一个用于删除物品的接口
export interface IDeleteItem {
    // 要删除的物品的唯一标识符
    itemid: number
}

// 定义一个用于下订单的接口
export interface IAddOrder {
    // 用户 ID
    user_id: number,
    // 物品 ID，与某个物品相关联
    itemid: number,
    // 购买数量
    quantity: number
    // 订单类型，可能是不同的类型，如租赁或购买
    order_type: string
    // 订单状态，可能有多种可能的状态
    status: string
    // 订单的总价格
    toal_price: number
    // 收货地址
    address: string
    // 联系电话
    phone: string
}

// 定义一个用于订单审核的接口
export interface IAuduitOrder {
    // 要审核的订单的标识符
    orderid: number
    // 订单的新状态，如 "已审核"、"未通过" 等
    status: string
}

// 定义一个用于获取特定状态订单的接口
export interface IGetAudtOrder {
    // 要获取的订单状态
    status: string
}

// 定义一个用于获取订单详情的接口
export interface IGetOrderDetal {
    // 订单的唯一标识符
    orderid: number
}

// 定义一个用于删除订单的接口
export interface IDeleteOrder {
    // 订单的 ID，用于标识要删除的订单
    orderid: number
}
