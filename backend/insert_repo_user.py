import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from dotenv import load_dotenv
import json
from datetime import datetime
from app.core.models.users import Users

# 加载环境变量
load_dotenv()

# 替换为你的实际数据库URL
DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL", "mysql+pymysql://root:yourpassword@localhost/coin"
)

# 创建引擎并连接到数据库
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化密码加密上下文，bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 哈希密码
hashed_password = pwd_context.hash("datawhale")

user_repo_dict = {}
with open("./github_data/all_repos_contributors.json", "r", encoding="utf-8") as f:
    all_repos_contributors = json.load(f)
    for repo in all_repos_contributors:
        for contributor in repo["contributors"]:
            repo_name = f"https://github.com/datawhalechina/{repo['repo_name']},\n"
            if contributor not in user_repo_dict:
                user_repo_dict[contributor] = repo_name
            else:
                user_repo_dict[contributor] += repo_name


"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(200), nullable=False)
    email = Column(VARCHAR(200), nullable=False)
    github = Column(VARCHAR(200))
    password = Column(VARCHAR(500), nullable=True)
    phone = Column(VARCHAR(80))
    gender = Column(VARCHAR(32))
    location = Column(VARCHAR(32))
    role = Column(VARCHAR(32))
    coin = Column(Float, default=0.0)
    avantar = Column(VARCHAR(256))
    desc = Column(VARCHAR(1000))
    register_time = Column(DateTime)
    last_login_time = Column(DateTime)
"""


# 插入数据的函数
def insert_data():
    session = SessionLocal()
    try:
        index = 1
        for user in list(user_repo_dict.keys()):
            print(f"Inserting {user} into database")

            str_index = str(index).zfill(4)
            phone_num = f"1581234{str_index}"
            github = f"https://github.com/{user}"
            value = user_repo_dict[user]
            desc = f"大家好，我是{user}。github:  {github}。\n我在以下仓库贡献了代码：\n{value}"

            # 使用ORM方式创建Users实例
            new_user = Users(
                username=user,
                phone=phone_num,
                github=github,
                role="developer",
                email=f"{user}@example.com",
                password=hashed_password,
                desc=desc,
                register_time=datetime.now(),  # 假设注册时间为当前时间
                last_login_time=datetime.now(),  # 假设最后登录时间为当前时间
            )

            # 添加到会话
            session.add(new_user)
            index += 1

        # 提交事务
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()  # 出现异常时回滚事务
        print(f"Error occurred: {e}")
    finally:
        session.close()  # 关闭会话


# 主函数
if __name__ == "__main__":
    insert_data()
