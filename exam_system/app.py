"""
Flask 应用主入口
"""
from flask import Flask, redirect, render_template
from flask_cors import CORS
from config import Config
from models import db
import pymysql

pymysql.install_as_MySQLdb()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    from api import bp as api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return redirect('/login')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app


def init_database():
    """初始化数据库表"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("数据库表创建成功！")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_database()
    else:
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
