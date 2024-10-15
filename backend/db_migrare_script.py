import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv(dotenv_path=".env.production")

# 从环境变量中获取 MySQL 连接字符串
mysql_connection_string = os.getenv("SQLALCHEMY_DATABASE_URL")

# SQLite 数据库文件的路径
sqlite_file_path = "./mydatabase.db"

# 连接到本地 SQLite 数据库
sqlite_conn = sqlite3.connect(sqlite_file_path)

# 创建 SQLAlchemy Engine 用于连接 MySQL
mysql_engine = create_engine(mysql_connection_string)

# 获取 SQLite 数据库中的所有表
sqlite_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(sqlite_tables_query, sqlite_conn)

migrated_tables = {'', 'consume', 'alembic_version', 'bill', 'apply', 'users'}

empty_tables = ['register', 'item', 'total_order', 'github_repos']

# 迁移所有非空且未迁移的表的数据
for table_name in tables["name"]:
    if table_name in migrated_tables:
        print(f"Table {table_name} is already migrated, skipping.")
        continue

    # 检查表是否为空
    count_query = f"SELECT COUNT(*) FROM {table_name}"
    count_result = pd.read_sql(count_query, sqlite_conn)
    record_count = count_result.iloc[0, 0]

    if record_count > 0:
        # 从 SQLite 中读取数据
        data = pd.read_sql(f"SELECT * FROM {table_name}", sqlite_conn)

        # 将数据写入 MySQL
        data.to_sql(table_name, mysql_engine, if_exists="replace", index=False)
        print(
            f"Table {table_name} with {record_count} records successfully migrated to MySQL."
        )

        # 更新迁移状态（如果需要持久化请考虑使用文件或数据库）
        migrated_tables.add(table_name)

    else:
        print(f"Table {table_name} is empty and was not migrated.")
        empty_tables.append(table_name)

# 关闭数据库连接
sqlite_conn.close()

print("Migration completed successfully.")
print(migrated_tables)
print(empty_tables)
