"""
数据库配置文件
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'exam-system-secret-key-2024'

    # 使用SQLite数据库（无需额外安装MySQL）
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 分页配置
    PAGE_SIZE = 20