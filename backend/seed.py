import sqlite3
import os
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash('zishu')
def create_directory(directory):  
    if not os.path.exists(directory):  
        os.makedirs(directory)
create_directory("static")
create_directory("static/profiles")
con = sqlite3.connect('mydatabase.db')
c = con.cursor()
sql = '''
INSERT INTO users (username, phone, role, email, password)
    VALUES ('管理员', '15812345678', 'admin', 'example@example.cn', %s);
'''% hashed_password
sql1 = '''
INSERT INTO users (username, phone, role, email, password)
    VALUES ('黎伟', '15821123639', 'developer', 'omige@live.cn', %s);
'''% hashed_password
# sql = '''
# INSERT INTO apply (user_id, repo, role, content, record_time)
#     VALUES (2, 'zishu', 'developer', 'pr_3', '2024-06-01');
# '''
# sql1 = '''
# INSERT INTO apply (user_id, repo, role, content, record_time)
#     VALUES (2, 'zishu', 'developer', 'issue_5', '2024-06-02');
# '''
c.execute(sql)
c.execute(sql1)
con.commit()
c.close()
con.close()