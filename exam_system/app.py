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
        # 自动添加缺失的列（兼容旧数据库）
        try:
            import sqlite3
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if db_uri.startswith('sqlite:///'):
                db_path = db_uri.replace('sqlite:///', '')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # 检查并添加 exams.shuffle_enabled
                cursor.execute("PRAGMA table_info(exams)")
                cols = [col[1] for col in cursor.fetchall()]
                if 'shuffle_enabled' not in cols:
                    cursor.execute("ALTER TABLE exams ADD COLUMN shuffle_enabled SMALLINT DEFAULT 0")
                    print("已添加 exams.shuffle_enabled 列")

                # 检查并添加 exam_records.shuffle_data
                cursor.execute("PRAGMA table_info(exam_records)")
                cols = [col[1] for col in cursor.fetchall()]
                if 'shuffle_data' not in cols:
                    cursor.execute("ALTER TABLE exam_records ADD COLUMN shuffle_data TEXT")
                    print("已添加 exam_records.shuffle_data 列")

                conn.commit()
                conn.close()
        except Exception as e:
            print(f"列迁移检查: {e}")

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
