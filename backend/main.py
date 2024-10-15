import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from app.routers import users
from app.routers import coin
from app.routers import item
from app.routers import update_data
from app.config import settings
from app.database import engine

app = FastAPI()

origins = [
    "http://christarter.com",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
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
        scheduler.add_job(
            update_repo, "interval", hours=0, minutes=0, seconds=15, id=job_id
        )

        # 直接返回字典
        return {"status": "success", "message": "Scheduled update started."}
    else:
        return {"status": "error", "message": "Scheduled update is already running."}


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
        print(f"stop update repo job {job_id}")
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
        print(f"execute update repo job {job_id}")
        return {
            "status": "success",
            "message": "Data update executed successfully. Please refresh the page to see new data.",
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": f"An error occurred while executing the update: {str(e)}",
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
