"""
数据库初始化脚本
"""
import pymysql
from config import Config


def create_database():
    """创建数据库"""
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        print(f"数据库 {Config.MYSQL_DB} 创建成功！")
    finally:
        connection.close()


def create_tables():
    """创建数据表"""
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role TINYINT DEFAULT 0 COMMENT '0学生，1管理员',
                    avatar VARCHAR(255),
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("表 users 创建成功")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    question_text TEXT NOT NULL,
                    option_a VARCHAR(255) NOT NULL,
                    option_b VARCHAR(255) NOT NULL,
                    option_c VARCHAR(255) NOT NULL,
                    option_d VARCHAR(255) NOT NULL,
                    answer CHAR(1) NOT NULL COMMENT 'A/B/C/D',
                    knowledge VARCHAR(100) COMMENT '知识点标签',
                    difficulty TINYINT DEFAULT 1 COMMENT '1简单，2中等，3困难',
                    score INT DEFAULT 2,
                    is_ai_generated TINYINT DEFAULT 0 COMMENT '0否，1是',
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("表 questions 创建成功")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exams (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    exam_name VARCHAR(100) NOT NULL,
                    total_score INT DEFAULT 0,
                    duration_minutes INT DEFAULT 60,
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("表 exams 创建成功")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exam_questions (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    exam_id INT NOT NULL,
                    question_id INT NOT NULL,
                    order_num INT DEFAULT 0,
                    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("表 exam_questions 创建成功")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exam_records (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    exam_id INT NOT NULL,
                    score INT DEFAULT 0,
                    total_score INT DEFAULT 0,
                    answers_detail TEXT COMMENT 'JSON格式存储答题详情',
                    wrong_questions TEXT COMMENT 'JSON格式存储错题ID列表',
                    start_time DATETIME,
                    end_time DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("表 exam_records 创建成功")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wrong_questions (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    question_id INT NOT NULL,
                    user_answer CHAR(1) COMMENT '用户当时选的答案',
                    ai_explanation TEXT COMMENT 'AI生成的讲解',
                    add_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("表 wrong_questions 创建成功")

        connection.commit()
        print("\n所有数据表创建成功！")
    finally:
        connection.close()


def insert_sample_data():
    """插入示例数据"""
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            import hashlib
            admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
            student_password = hashlib.sha256('student123'.encode()).hexdigest()

            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO users (username, password, role) VALUES
                    ('admin', %s, 1),
                    ('2024001', %s, 0),
                    ('2024002', %s, 0)
                """, (admin_password, student_password, student_password))
                print("示例用户创建成功")

            cursor.execute("SELECT COUNT(*) FROM questions")
            if cursor.fetchone()[0] == 0:
                sample_questions = [
                    ("Python中，以下哪个关键字用于定义函数？", "def", "function", "define", "lambda", "A", "Python基础", 1, 2),
                    ("以下哪个不是Python的数据类型？", "int", "str", "char", "list", "C", "Python基础", 1, 2),
                    ("Python中，列表和元组的主要区别是什么？", "列表可变，元组不可变", "列表不可变，元组可变", "没有区别", "列表只能存数字", "A", "Python数据结构", 2, 2),
                    ("如何使用for循环遍历1到10？", "for i in range(1,10)", "for i in range(1,11)", "for i in [1,10]", "for i in 1..10", "B", "Python循环", 1, 2),
                    ("以下哪个方法可以向列表末尾添加元素？", "insert()", "append()", "add()", "push()", "B", "Python数据结构", 1, 2),
                    ("Python中，如何定义一个类？", "class MyClass:", "define MyClass:", "new class MyClass", "Class MyClass", "A", "Python面向对象", 2, 2),
                    ("以下哪个模块用于处理JSON数据？", "json", "math", "random", "os", "A", "Python标准库", 1, 2),
                    ("如何创建一个字典？", "{}", "[]", "()", "<>", "A", "Python数据结构", 1, 2),
                    ("Python中，self的作用是什么？", "引用对象本身", "引用父类", "定义私有变量", "导入模块", "A", "Python面向对象", 2, 2),
                    ("以下哪个是Python的继承语法？", "class Child(Parent):", "class Child extends Parent:", "class Child <- Parent", "class Child:Parent", "A", "Python面向对象", 2, 2),
                ]

                for q in sample_questions:
                    cursor.execute("""
                        INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, answer, knowledge, difficulty, score)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, q)
                print("示例题目创建成功")

        connection.commit()
        print("\n示例数据插入成功！")
    finally:
        connection.close()


if __name__ == '__main__':
    print("=" * 50)
    print("开始初始化数据库...")
    print("=" * 50)

    create_database()
    create_tables()
    insert_sample_data()

    print("\n" + "=" * 50)
    print("数据库初始化完成！")
    print("=" * 50)
    print("\n默认账户：")
    print("  管理员: admin / admin123")
    print("  学生: 2024001 / student123 或 2024002 / student123")
