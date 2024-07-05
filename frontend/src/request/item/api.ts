import instance from "../base";
import  * as Item from "./type";
export const getItemAPI = (): Promise<any> =>
    instance.get("/api/item/get_item");
export const getItemDetal=(data: Item.IGetItemDetal): Promise<any>=>
    instance.post("/api/item/get_item_detal", data)
export const addItemAPI = (data: Item.IAddItem): Promise<any> =>
    instance.post("/api/item/add_item", data);

export const deleteItemAPI = (data: Item.IDeleteItem): Promise<any> =>
    instance.post("/api/item/delete_item", data);
export const getOrderAPI = (): Promise<any> =>
    instance.get("/api/item/get_order");

export const addOrderAPI = (data: Item.IAddOrder): Promise<any> =>
    instance.post("/api/item/add_order", data);

export const auduitOrderAPI = (data: Item.IAuduitOrder): Promise<any> =>
    instance.post("/api/item/auduit_order", data);

export const getAuditOrderAPI = (data: Item.IGetAudtOrder): Promise<any> =>
    instance.post("/api/item/get_audit_order",data);

export const getOrderDetalAPI = (data: Item.IGetOrderDetal): Promise<any> =>
    instance.post("/api/item/get_order_detal", data);

export const deleteOrderAPI = (data: Item.IDeleteOrder): Promise<any> =>
    instance.post("/api/item/delete_order", data);
export const getUserOrderAPI =(): Promise<any> =>
    instance.get("/api/item/get_user_order");