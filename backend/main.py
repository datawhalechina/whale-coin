import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import  BackgroundTasks
from app.routers import users
from app.routers import coin
from app.routers import item
from app.routers import update_data
from app.config import settings
from app.database import engine

app = FastAPI()
app.mount("/api/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)

app.include_router(users.router)
app.include_router(coin.coin)
app.include_router(item.item)
# app.include_router(update_data.router) 


@app.get("/")
def read_root():
    return {"Hello": "World"}


users.Base.metadata.create_all(bind=engine)
coin.Base.metadata.create_all(bind=engine)
item.Base.metadata.create_all(bind=engine)



from apscheduler.schedulers.background import BackgroundScheduler
from typing import List, Dict
import requests
import threading
import asyncio


# 初始化APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# 任务函数，用于定时抓取GitHub issues
from update_repo import update_repo
from update_repo import get_current_time
import time
# 为定时任务分配一个唯一的ID
job_id = "update_repo_job"

@app.get("/start-scheduled-update")
async def start_scheduled_update():
    """
    启动定时任务，定期更新 GitHub 仓库的 issues。
    """
    job = scheduler.get_job(job_id)
    
    if job is None:
        # 立即运行任务并获取结果（假设 update_repo 返回更新数据）
        update_repo()  
        
        # 添加定时任务
        scheduler.add_job(update_repo, 'interval', hours=0, minutes=0, seconds=15, id=job_id)
        
        # 直接返回字典
        return {
            "status": "success",
            "message": "Scheduled update started."
        }
    else:
        return {
            "status": "error",
            "message": "Scheduled update is already running."
        }


@app.get("/is-scheduled-update-running")
async def is_scheduled_update_running():
    """
    检查是否有定时拉取任务正在运行
    """
    job = scheduler.get_job(job_id)
    if job:
        return {"is_running": True}
    else:
        return {"is_running": False}


@app.get("/stop-scheduled-update")
async def stop_scheduled_update():
    """
    停止当前运行的定时拉取任务
    """
    job = scheduler.get_job(job_id)
    if job is not None:
        scheduler.remove_job(job_id)
        print(f'stop update repo job {job_id}')
        return {"message": "Scheduled update stopped."}
    else:
        return {"message": "No update task is currently running."}


@app.get("/execute-update")
async def execute_update():
    """
    手动执行数据更新任务，将数据写入数据库，并通知前端刷新
    """
    try:

        update_repo()
        print(f'execute update repo job {job_id}')
        return {"status":"success","message": "Data update executed successfully. Please refresh the page to see new data."}
    except Exception as e:
        return {"status":"failed","message": f"An error occurred while executing the update: {str(e)}"}

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,reload=True)