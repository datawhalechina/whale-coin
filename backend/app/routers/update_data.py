from fastapi import FastAPI, APIRouter
from threading import Lock
import subprocess


router = APIRouter()

# 用于存储子进程的实例
process = None
# 互斥锁，用于线程同步
lock = Lock()

@router.get("/start-update")
async def start_update():
    global process
    with lock:
        if process is not None and process.poll() is None:
            return {"message": "Update process is already running."}

        try:
            # 启动子进程以运行脚本
            process = subprocess.Popen(["python", "update_repo.py"])
            return {"message": "Update process started successfully."}
        except Exception as e:
            return {"error": str(e)}

@router.get("/check-update-status")
async def check_update_status():
    with lock:
        # 检查子进程是否正在运行
        if process is not None and process.poll() is None:
            return {"is_running": True}
        return {"is_running": False}



# 运行 FastAPI
# 使用命令 'uvicorn <your_script_name>:app --reload' 来启动服务
