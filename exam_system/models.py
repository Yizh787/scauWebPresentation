"""
数据库模型
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.SmallInteger, default=0)
    avatar = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'avatar': self.avatar,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(1), nullable=False)
    knowledge = db.Column(db.String(100))
    difficulty = db.Column(db.SmallInteger, default=1)
    score = db.Column(db.Integer, default=2)
    is_ai_generated = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'answer': self.answer,
            'knowledge': self.knowledge,
            'difficulty': self.difficulty,
            'score': self.score,
            'is_ai_generated': self.is_ai_generated,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }


class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_name = db.Column(db.String(100), nullable=False)
    total_score = db.Column(db.Integer, default=0)
    duration_minutes = db.Column(db.Integer, default=60)
    shuffle_enabled = db.Column(db.SmallInteger, default=0)  # 0=关闭乱序 1=开启乱序
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'exam_name': self.exam_name,
            'total_score': self.total_score,
            'duration_minutes': self.duration_minutes,
            'shuffle_enabled': self.shuffle_enabled,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }


class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    order_num = db.Column(db.Integer, default=0)


class ExamRecord(db.Model):
    __tablename__ = 'exam_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    answers_detail = db.Column(db.Text)
    wrong_questions = db.Column(db.Text)
    shuffle_data = db.Column(db.Text)  # 存储题目乱序和选项乱序映射（JSON）
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'exam_id': self.exam_id,
            'score': self.score,
            'total_score': self.total_score,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None
        }


class WrongQuestion(db.Model):
    __tablename__ = 'wrong_questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.String(1))
    ai_explanation = db.Column(db.Text)
    add_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'ai_explanation': self.ai_explanation,
            'add_time': self.add_time.strftime('%Y-%m-%d %H:%M:%S') if self.add_time else None
        }
