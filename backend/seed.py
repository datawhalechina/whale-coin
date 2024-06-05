import sqlite3
import os
def create_directory(directory):  
    if not os.path.exists(directory):  
        os.makedirs(directory)
create_directory("static")
create_directory("static/profiles")
con = sqlite3.connect('mydatabase.db')
c = con.cursor()
# sql = '''
# INSERT INTO users (username, phone, role, email, password)
#     VALUES ('管理员', '15812345678', 'admin', 'example@example.cn', '$2b$12$6S.75dg0aeWpnu8ZqJso/.fV6QSoe8Qz4WXpkHlTnAeHZq1b1x3n2');
# '''
# sql1 = '''
# INSERT INTO users (username, phone, role, email, password)
#     VALUES ('黎伟', '15821123639', 'developer', 'omige@live.cn', '$2b$12$6S.75dg0aeWpnu8ZqJso/.fV6QSoe8Qz4WXpkHlTnAeHZq1b1x3n2');
# '''
sql = '''
INSERT INTO apply (user_id, repo, role, content, record_time)
    VALUES (2, 'zishu', 'developer', 'pr_3', '2024-06-01');
'''
sql1 = '''
INSERT INTO apply (user_id, repo, role, content, record_time)
    VALUES (2, 'zishu', 'developer', 'issue_5', '2024-06-02');
'''
c.execute(sql)
c.execute(sql1)
con.commit()
c.close()
con.close()