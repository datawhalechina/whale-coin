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


// 启动定时更新任务的API请求
export const startScheduledUpdateAPI = (): Promise<any> => 
    instance.get("/start-scheduled-update");

// 检查定时更新任务是否运行的API请求
export const isScheduledUpdateRunningAPI = (): Promise<any> => 
    instance.get("/is-scheduled-update-running");

// 停止定时更新任务的API请求
export const stopScheduledUpdateAPI = (): Promise<any> => 
    instance.get("/stop-scheduled-update");

// 手动执行更新任务并写入数据库的API请求
export const executeUpdateAPI = (): Promise<any> => 
    instance.get("/execute-update");