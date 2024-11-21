import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
from app.routers import coin
from app.routers import item
from app.config import settings
from app.database import engine
from datetime import datetime
import logging
app = FastAPI()

origins = [
    "http://christarter.com:8008",
    "http://localhost:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# 初始化APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# 任务函数，用于定时抓取GitHub issues
from update_repo import update_repo, update_repo_by_multithreaded


# 为定时任务分配一个唯一的ID
job_id = "update_repo_job"

@app.get("/start-scheduled-update")
async def start_scheduled_update():
    """
    启动定时任务，定期更新 GitHub 仓库的 issues。
    """
    job = scheduler.get_job(job_id)
    if job is None:
        new_job = scheduler.add_job(
            update_repo_by_multithreaded, "interval", hours=1, minutes=0, seconds=0, id=job_id
        )
        next_run_time = new_job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if new_job.next_run_time else "Unknown"
        logging.info(f"Scheduled update started. Next run time: {next_run_time}.")
        return {"status": "success", "message": f"Scheduled update started. Next run time: {next_run_time}."}
    else:
        next_run_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else "Unknown"
        logging.warning(f"Scheduled update is already running. Next run time: {next_run_time}.")
        return {"status": "error", "message": f"Scheduled update is already running. Next run time: {next_run_time}."}




@app.get("/is-scheduled-update-running")
async def is_scheduled_update_running():
    """
    检查是否有定时拉取任务正在运行，并返回下次运行时间。
    """
    job = scheduler.get_job(job_id)
    if job:
        next_run_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else "Unknown"
        logging.info(f"Checked scheduled update running status: True. Next run time: {next_run_time}.")
        return {"is_running": True, "next_run_time": next_run_time}
    else:
        logging.info("Checked scheduled update running status: False.")
        return {"is_running": False, "next_run_time": None}


@app.get("/stop-scheduled-update")
async def stop_scheduled_update():
    """
    停止当前运行的定时拉取任务，并显示下次运行时间（如适用）。
    """
    job = scheduler.get_job(job_id)
    if job is not None:
        next_run_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else "Unknown"
        scheduler.remove_job(job_id)
        logging.info(f"Stopped scheduled update: {job_id}. Next run time was: {next_run_time}.")
        return {"message": f"Scheduled update stopped. Next run time was: {next_run_time}."}
    else:
        logging.warning("No update task is currently running.")
        return {"message": "No update task is currently running."}


@app.get("/execute-update")
def execute_update():
    """
    手动执行数据更新任务，将数据写入数据库，并通知前端刷新。记录当前时间。
    """
    try:
        # update_repo()
        update_repo_by_multithreaded()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Executed manual update successfully at {current_time}.")
        return {
            "status": "success",
            "message": f"Data update executed successfully at {current_time}.",
        }
    except Exception as e:
        logging.error(f"An error occurred while executing the update: {str(e)}")
        return {
            "status": "failed",
            "message": f"An error occurred while executing the update: {str(e)}",
        }
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=False,workers=1)
