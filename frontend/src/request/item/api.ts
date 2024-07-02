import instance from "../base";
import  * as Item from "./type";
export const fetchItemAPI = (): Promise<any> =>
    instance.get("/api/item/fetch_item");

export const addItemAPI = (data: Item.IAddItem): Promise<any> =>
    instance.post("/api/item/add_item", data);

export const getOrderAPI = (): Promise<any> =>
    instance.get("/api/item/get_order");

export const addOrderAPI = (data: Item.IaddOrder): Promise<any> =>
    instance.post("/api/item/handle_supervise", data);

export const auduitOrderAPI = (data: Item.IAuduitOrder): Promise<any> =>
    instance.post("/api/item/auduit_order", data);

export const getAuditOrderAPI = (data: Item.IGetAudtOrder): Promise<any> =>
    instance.get("/api/item/get_audit_order");