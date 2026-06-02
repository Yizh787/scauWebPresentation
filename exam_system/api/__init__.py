"""
API 蓝图初始化
"""
from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from api import auth, exam, ai
