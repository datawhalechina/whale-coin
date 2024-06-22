import instance from "../base";
import  * as Coin from "./type";
export const fetchApplyAPI = (): Promise<any> =>
    instance.get("/api/coin/fetch_apply");

export const handleApplyAPI = (data: Coin.IHandleApply): Promise<any> =>
    instance.post("/api/coin/handle_apply", data);

export const fetchSuperviseAPI = (): Promise<any> =>
    instance.get("/api/coin/fetch_supervise");

export const fetchAllSuperviseAPI = (): Promise<any> =>
    instance.get("/api/coin/fetch_all_supervise");

export const handleSuperviseAPI = (data: Coin.IHandleSupervise): Promise<any> =>
    instance.post("/api/coin/handle_supervise", data);

export const fetchConsumeAPI = (): Promise<any> =>
    instance.get("/api/coin/fetch_consume");

export const handleConsumeAPI = (data: Coin.IHandleConsume): Promise<any> =>
    instance.post("/api/coin/handle_consume", data);

export const addEventAPI = (data: Coin.IAddEvent): Promise<any> =>
    instance.post("/api/coin/add_event", data);

export const fetchBillAPI = (): Promise<any> =>
    instance.get("/api/coin/fetch_bill");