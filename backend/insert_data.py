import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 替换为你的实际数据库URL
DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', 'mysql+pymysql://root:yourpassword@localhost/coin')

# 创建引擎并连接到数据库
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化密码加密上下文，bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 哈希密码
hashed_password = pwd_context.hash('zishu')

# 定义SQL语句
# sql = '''
# INSERT INTO apply (user_id, repo, role, content, record_time)
#     VALUES (2, 'zishu', 'developer', 'pr_3', '2024-06-01');
# '''

# sql1 = '''
# INSERT INTO apply (user_id, repo, role, content, record_time)
#     VALUES (2, 'zishu', 'developer', 'issue_5', '2024-06-02');
# '''

sql2 = f'''
INSERT INTO users (username, phone, role, email, password)
    VALUES ('管理员', '15812345612', 'fxy', 'example@example.cn', '{hashed_password}');
'''

# 插入数据的函数
def insert_data():
    session = SessionLocal()
    try:
        # session.execute(text(sql))
        # session.execute(text(sql1))
        session.execute(text(sql2))
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# 主函数
if __name__ == "__main__":
    insert_data()
