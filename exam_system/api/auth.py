"""
登录注册接口
"""
from flask import request, jsonify
from api import bp
from models import db, User
import hashlib
import re


def hash_password(password):
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_username(username):
    """验证用户名格式（学号或手机号）"""
    if not username or len(username) < 4:
        return False
    return True


def validate_password(password):
    """验证密码格式（至少6位）"""
    if not password or len(password) < 6:
        return False
    return True


@bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')
    role = data.get('role', 0)

    if not validate_username(username):
        return jsonify({'code': 400, 'message': '用户名格式错误（至少4位）'}), 400

    if not validate_password(password):
        return jsonify({'code': 400, 'message': '密码至少6位'}), 400

    if role not in [0, 1]:
        role = 0

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'code': 409, 'message': '用户名已存在'}), 409

    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '注册成功',
        'data': {
            'user_id': new_user.id,
            'username': new_user.username,
            'role': new_user.role
        }
    })


@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

    hashed_password = hash_password(password)

    user = User.query.filter_by(username=username, password=hashed_password).first()

    if not user:
        return jsonify({'code': 401, 'message': '用户名或密码错误'}), 401

    return jsonify({
        'code': 200,
        'message': '登录成功',
        'data': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'avatar': user.avatar
        }
    })


@bp.route('/user/info', methods=['GET'])
def get_user_info():
    """获取用户信息"""
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    return jsonify({
        'code': 200,
        'data': user.to_dict()
    })


@bp.route('/user/update', methods=['POST'])
def update_user():
    """更新用户信息"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    if 'avatar' in data:
        user.avatar = data['avatar']

    if 'password' in data and data['password']:
        if validate_password(data['password']):
            user.password = hash_password(data['password'])
        else:
            return jsonify({'code': 400, 'message': '密码至少6位'}), 400

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '更新成功',
        'data': user.to_dict()
    })
