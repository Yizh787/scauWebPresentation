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

    @app.route('/admin/admin_dashboard.html')
    def admin_dashboard():
        return render_template('admin/admin_dashboard.html')

    @app.route('/student/student_dashboard.html')
    def student_dashboard():
        return render_template('student/student_dashboard.html')

    @app.route('/student/exam.html')
    def exam_page():
        return render_template('student/exam.html')

    @app.route('/student/exam_result.html')
    def exam_result():
        return render_template('student/exam_result.html')

    @app.route('/student/wrong_explain.html')
    def wrong_explain():
        return render_template('student/wrong_explain.html')

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app


def init_database():
    """初始化数据库表并添加默认管理员账号"""
    app = create_app()
    with app.app_context():
        db.create_all()
        
        from models import User
        import hashlib
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
            admin = User(username='admin', password=hashed_password, role=1)
            db.session.add(admin)
            db.session.commit()
            print("管理员账号创建成功：用户名 admin，密码 admin123")
        
        print("数据库表创建成功！")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_database()
    else:
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
