import time

from app.database import Base, engine, SessionLocal
from app.core.models.coin import Apply
from app.core.models.users import Users
from datetime import datetime
from get_repo_oauth import get_all_repos, get_all_issues_and_prs
from apscheduler.schedulers.background import BackgroundScheduler
import logging
# from app.config import settings
import os
from get_repo_oauth import save_info_to_json
import json
from app.config import settings

# from insert_repo_user import hashed_password
from passlib.context import CryptContext
import time




import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles


# 初始化密码加密上下文，bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 哈希密码
hashed_password = pwd_context.hash("datawhale")
print(f"hashed_password: {hashed_password}")


# 保存列表到json文件
def save_list_to_json(list_data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        data = list(list_data)
        data.sort()
        json.dump(data, f, ensure_ascii=False, indent=4)


# 获取当前时间
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 伪更新函数
def update_repo_test():
    time_now = get_current_time()
    print(f"time now is {time_now}")

    # 数据列表，模拟更新结果
    updated_data = []

    for i in range(10):
        print(f"Updating repo {i}...")
        time.sleep(1)

        # 添加每次更新的结果到列表中
        updated_data.append(f"Update {i + 1} completed at {get_current_time()}")

    # 返回更新的数据
    return updated_data


def update_repo():
    username = "datawhalechina"
    Base.metadata.create_all(engine)
    db = SessionLocal()

    if os.path.exists("./github_data/all_issues.json"):
        with open("./github_data/all_issues.json", "r", encoding="utf-8") as f:
            all_issues = set(json.load(f))
    else:
        all_issues = set()

    # 获取所有仓库信息
    if not os.path.exists("./github_data/all_repos.json"):
        repos = get_all_repos("datawhalechina")
        save_info_to_json(repos, "./github_data/all_repos.json")
    else:
        with open("./github_data/all_repos.json", "r", encoding="utf-8") as f:
            repos = json.load(f)

    # 获取每个仓库的所有issues和PRs
    #TODO: 停止更新 需要改为异步数据库插入操作
    if repos != "Error: Unable to fetch repositories":
        logging.info(f"lth repos {len(repos)}")
        for index, repo in enumerate(repos[:]):

            repo_name = repo["name"]
            logging.info(f"{index} repo: {repo_name}")
            total_issues = get_all_issues_and_prs(username, repo_name,page=1)
            logging.info("total_issues count: %d", len(total_issues))
            for issue in total_issues[:]:
                url = issue["html_url"]
                all_issues.add(url)
                logging.info(f"{url}")
                issue_data = db.query(Apply).filter(Apply.url == url).first()
                if issue_data:
                    logging.info(f"已存在")
                else:
                    # 获取数据表Users的数量
                    user_count = db.query(Users).count()
                    phone_number = 15812340000 + user_count - 2
                    logging.info(f"phone_number {phone_number}")
                    # 如果数据表中没有该issue，则插入新数据
                    try:
                        user_id = (
                            db.query(Users)
                            .filter_by(username=issue["user"]["login"])
                            .first()
                        )
                        if not user_id:
                            new_user = Users(
                                username=issue["user"]["login"],
                                phone=f"{phone_number}",
                                github=issue["user"]["html_url"],
                                role="developer",
                                email=f'{issue["user"]["login"]}@example.com',
                                password=hashed_password,
                                desc=f"我为项目{repo_name}贡献了一个issue",
                                register_time=datetime.now(),
                                last_login_time=datetime.now(),
                            )
                            db.add(new_user)
                            db.commit()
                            logging.info(f"Inserted new user: {new_user.username}")
                            user_id = new_user.id
                        else:
                            user_id = user_id.id
                        logging.info(f"user id {user_id}")
                        repo_apply = Apply(
                            user_id=user_id,
                            repo=repo_name,
                            role="developer",
                            repo_owner_name=username,
                            user_name=issue["user"]["login"],
                            pid=issue["number"],
                            title=issue["title"],
                            url=url,
                            content=issue["body"],
                            state=issue["state"],
                            record_time=datetime.strptime(
                                issue["created_at"][:-1], "%Y-%m-%dT%H:%M:%S"
                            ),
                        )
                        db.add(repo_apply)
                        # db.commit()
                        logging.info(f"Inserted new url: {url}")
                    except Exception as e:
                        logging.error(f"error: {e}")
                        pass

            db.commit()
            time.sleep(5)
    save_list_to_json(all_issues, "./github_data/all_issues.json")
    db.close()


async def update_repo1():
    username = "datawhalechina"
    # 假设你使用的是异步的数据库引擎
    async with AsyncSession(engine) as session:
        db = session

        # 异步读取 issues 文件
        if os.path.exists("./github_data/all_issues.json"):
            async with aiofiles.open("./github_data/all_issues.json", "r", encoding="utf-8") as f:
                contents = await f.read()
                all_issues = set(json.loads(contents))
        else:
            all_issues = set()

        # 异步读取仓库信息
        if not os.path.exists("./github_data/all_repos.json"):
            repos = await get_all_repos("datawhalechina")
            await save_info_to_json(repos, "./github_data/all_repos.json")
        else:
            async with aiofiles.open("./github_data/all_repos.json", "r", encoding="utf-8") as f:
                repos = json.loads(await f.read())

        # 处理每个仓库的 issues 和 PRs
        if repos != "Error: Unable to fetch repositories":
            logging.info(f"lth repos {len(repos)}")
            for index, repo in enumerate(repos[:]):

                repo_name = repo["name"]
                logging.info(f"{index} repo: {repo_name}")
                total_issues = await get_all_issues_and_prs(username, repo_name)
                logging.info("total_issues count: %d", len(total_issues))
                for issue in total_issues[:]:
                    url = issue["html_url"]
                    all_issues.add(url)
                    logging.info(f"{url}")
                    issue_data = await db.execute(
                        db.query(Apply).filter(Apply.url == url)
                    )
                    if issue_data:
                        logging.info(f"{issue_data.url} 已存在")
                    else:
                        # 获取数据表Users的数量
                        user_count = (await db.execute(db.query(Users).count())).scalar()
                        phone_number = 15812340000 + user_count - 2
                        logging.info(f"phone_number {phone_number}")
                        # 如果数据表中没有该 issue，则插入新数据
                        try:
                            user_id = await db.execute(
                                db.query(Users).filter_by(username=issue["user"]["login"])
                            )
                            if not user_id:
                                new_user = Users(
                                    username=issue["user"]["login"],
                                    phone=f"{phone_number}",
                                    github=issue["user"]["html_url"],
                                    role="developer",
                                    email=f'{issue["user"]["login"]}@example.com',
                                    password=hashed_password,
                                    desc=f"我为项目{repo_name}贡献了一个issue",
                                    register_time=datetime.now(),
                                    last_login_time=datetime.now(),
                                )
                                db.add(new_user)
                                await db.commit()
                                logging.info(f"Inserted new user: {new_user.username}")
                                user_id = new_user.id
                            else:
                                user_id = user_id.id
                            logging.info(f"user id {user_id}")
                            repo_apply = Apply(
                                user_id=user_id,
                                repo=repo_name,
                                role="developer",
                                repo_owner_name=username,
                                user_name=issue["user"]["login"],
                                pid=issue["number"],
                                title=issue["title"],
                                url=url,
                                content=issue["body"],
                                state=issue["state"],
                                record_time=datetime.strptime(
                                    issue["created_at"][:-1], "%Y-%m-%dT%H:%M:%S"
                                ),
                            )
                            db.add(repo_apply)
                            await db.commit()
                            logging.info(f"Inserted new url: {url}")
                        except Exception as e:
                            logging.error(f"error: {e}")
                            pass

                await asyncio.sleep(5)  # 异步睡眠，不阻塞
        await save_list_to_json(all_issues, "./github_data/all_issues.json")



if __name__ == "__main__":
    print("update repo begin")
    update_repo()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     update_repo,
    #     "cron",
    #     hour=settings.UPDATAREPO_STARTTIMEHOUR,
    #     minute=settings.UPDATAREPO_STARTTIMEMINUTE,
    #     second=settings.UPDATAREPO_STARTTIMESECOND,
    # )
    # scheduler.start()
    # try:
    #     while True:
    #         time.sleep(12)  # 模拟主程序正在运行的其他任务
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
