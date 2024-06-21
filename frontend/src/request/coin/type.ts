export interface IHandleApply {
    action:string
    id:number
}

export interface IHandleSupervise {
    action:string
    notes:string
    id:number
    amount:number
}

export interface IHandleConsume {
    user_id: number
    content: string
    amount:number
}

export interface IAddEvent {
    user_id: number
    content: string
    amount:number
}