from fastapi import APIRouter
import subprocess

router = APIRouter()


@router.get("/start-update")
async def start_update():
    try:
        subprocess.Popen(["python", "update_repo.py"])
        return {"message": "Update process started successfully."}
    except Exception as e:
        return {"error": str(e)}
