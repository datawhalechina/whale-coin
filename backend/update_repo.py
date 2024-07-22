import time

from app.database import Base, engine, SessionLocal
from app.core.models.coin import Apply
from datetime import datetime
from get_repo_oauth import get_all_repos, get_all_issues_and_prs
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings


def update_repo():

    username = 'datawhalechina'
    Base.metadata.create_all(engine)
    db = SessionLocal()

    # 获取所有仓库信息
    repos = get_all_repos(username)
    # 获取每个仓库的所有issues和PRs
    if repos != "Error: Unable to fetch repositories":
        for repo in repos:
            if repo['name'] == "zishu":
                issues, prs = get_all_issues_and_prs(username, repo['name'])
                for issue in issues:
                    user = db.query(Apply).filter(Apply.content == issue['html_url'],
                                                  Apply.state == issue['state']).first()
                    if not user:
                        repo_apply = Apply(
                            repo=repo['name'],
                            repo_owner_name=username,
                            user_name=issue['user']['login'],
                            pid=issue['number'],
                            title=issue['title'],
                            content=issue['html_url'],
                            state=issue['state'],
                            record_time=datetime.strptime(issue['created_at'][:-1], '%Y-%m-%dT%H:%M:%S')
                        )
                        db.add(repo_apply)
                    db.commit()


if __name__ == "__main__":

    update_repo()
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_repo, 'cron', hour=settings.UPDATAREPO_STARTTIMEHOUR, minute=settings.UPDATAREPO_STARTTIMEMINUTE, second=settings.UPDATAREPO_STARTTIMESECOND)
    scheduler.start()
    try:
        while True:
            time.sleep(12)  # 模拟主程序正在运行的其他任务
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


