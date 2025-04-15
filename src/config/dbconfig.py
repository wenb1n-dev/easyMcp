import os
from dotenv import load_dotenv

def get_config():
    """从环境变量获取数据库配置信息

    返回:
        dict: 包含数据库连接所需的配置信息
        - host: 数据库主机地址
        - port: 数据库端口
        - user: 数据库用户名
        - password: 数据库密码
        - database: 数据库名称
        - role: 数据库角色权限

    异常:
        ValueError: 当必需的配置信息缺失时抛出
    """
    # 加载.env文件
    load_dotenv()

    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
        "role": os.getenv("MYSQL_ROLE", "readonly")  # 默认为只读角色
    }
    
    if not all([config["user"], config["password"], config["database"]]):
        raise ValueError("缺少必需的数据库配置")

    return config