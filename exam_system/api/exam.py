"""
考试相关接口
"""
from flask import request, jsonify
from api import bp
from models import db, Exam, ExamQuestion, ExamRecord, Question, WrongQuestion, User
from datetime import datetime
import json


@bp.route('/exams', methods=['GET'])
def get_exams():
    """获取考试列表（可选 user_id 排除已完成）"""
    user_id = request.args.get('user_id')

    exams = Exam.query.order_by(Exam.create_time.desc()).all()

    if user_id:
        completed_ids = {
            r.exam_id for r in ExamRecord.query.filter_by(user_id=int(user_id)).filter(ExamRecord.end_time.isnot(None)).all()
        }
        exams = [e for e in exams if e.id not in completed_ids]

    return jsonify({
        'code': 200,
        'data': [exam.to_dict() for exam in exams]
    })


@bp.route('/exam/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    """获取考试详情（含题目）"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'code': 404, 'message': '考试不存在'}), 404

    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(ExamQuestion.order_num).all()

    questions = []
    for eq in exam_questions:
        question = Question.query.get(eq.question_id)
        if question:
            questions.append(question.to_dict())

    return jsonify({
        'code': 200,
        'data': {
            'exam': exam.to_dict(),
            'questions': questions
        }
    })


@bp.route('/exam/create', methods=['POST'])
def create_exam():
    """创建考试（管理员）"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    exam_name = data.get('exam_name', '').strip()
    duration_minutes = data.get('duration_minutes', 60)
    question_ids = data.get('question_ids', [])

    if not exam_name:
        return jsonify({'code': 400, 'message': '考试名称不能为空'}), 400

    if not question_ids:
        return jsonify({'code': 400, 'message': '请选择至少一道题目'}), 400

    total_score = 0
    for qid in question_ids:
        question = Question.query.get(qid)
        if question:
            total_score += question.score

    new_exam = Exam(
        exam_name=exam_name,
        duration_minutes=duration_minutes,
        total_score=total_score
    )
    db.session.add(new_exam)
    db.session.flush()

    for idx, qid in enumerate(question_ids):
        eq = ExamQuestion(exam_id=new_exam.id, question_id=qid, order_num=idx + 1)
        db.session.add(eq)

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '考试创建成功',
        'data': new_exam.to_dict()
    })


@bp.route('/exam/start', methods=['POST'])
def start_exam():
    """开始考试"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    user_id = data.get('user_id')
    exam_id = data.get('exam_id')

    if not user_id or not exam_id:
        return jsonify({'code': 400, 'message': '参数不完整'}), 400

    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    exam = Exam.query.get(int(exam_id))
    if not exam:
        return jsonify({'code': 404, 'message': '考试不存在'}), 404

    existing_record = ExamRecord.query.filter_by(user_id=user_id, exam_id=exam_id, end_time=None).first()
    if existing_record:
        return jsonify({
            'code': 200,
            'message': '继续考试',
            'data': {
                'record_id': existing_record.id,
                'exam': exam.to_dict()
            }
        })

    record = ExamRecord(
        user_id=user_id,
        exam_id=exam_id,
        total_score=exam.total_score,
        start_time=datetime.now()
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '考试开始',
        'data': {
            'record_id': record.id,
            'exam': exam.to_dict()
        }
    })


@bp.route('/exam/submit', methods=['POST'])
def submit_exam():
    """提交考试"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    record_id = data.get('record_id')
    answers = data.get('answers', [])

    if not record_id:
        return jsonify({'code': 400, 'message': '考试记录ID不能为空'}), 400

    record = ExamRecord.query.get(int(record_id))
    if not record:
        return jsonify({'code': 404, 'message': '考试记录不存在'}), 404

    if record.end_time:
        return jsonify({'code': 400, 'message': '考试已提交'}), 400

    exam = Exam.query.get(record.exam_id)
    exam_questions = ExamQuestion.query.filter_by(exam_id=record.exam_id).order_by(ExamQuestion.order_num).all()

    score = 0
    wrong_list = []

    for eq in exam_questions:
        question = Question.query.get(eq.question_id)
        if not question:
            continue

        user_answer = None
        for ans in answers:
            if ans.get('question_id') == question.id:
                user_answer = ans.get('answer')
                break

        if user_answer and user_answer.upper() == question.answer.upper():
            score += question.score
        else:
            wrong_list.append(question.id)

            wrong_q = WrongQuestion.query.filter_by(user_id=record.user_id, question_id=question.id).first()
            if not wrong_q:
                wrong_q = WrongQuestion(
                    user_id=record.user_id,
                    question_id=question.id,
                    user_answer=user_answer or '',
                    add_time=datetime.now()
                )
                db.session.add(wrong_q)

    record.score = score
    record.answers_detail = json.dumps(answers, ensure_ascii=False)
    record.wrong_questions = json.dumps(wrong_list, ensure_ascii=False)
    record.end_time = datetime.now()

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '提交成功',
        'data': {
            'score': score,
            'total_score': record.total_score,
            'wrong_count': len(wrong_list)
        }
    })


@bp.route('/exam/records', methods=['GET'])
def get_exam_records():
    """获取用户的考试记录"""
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400

    records = ExamRecord.query.filter_by(user_id=int(user_id)).order_by(ExamRecord.start_time.desc()).all()

    result = []
    for record in records:
        exam = Exam.query.get(record.exam_id)
        result.append({
            'record': record.to_dict(),
            'exam_name': exam.exam_name if exam else '未知考试'
        })

    return jsonify({
        'code': 200,
        'data': result
    })


@bp.route('/exam/records/all', methods=['GET'])
def get_all_exam_records():
    """获取所有学生的考试记录（管理员）"""
    records = ExamRecord.query.filter(ExamRecord.end_time.isnot(None)).order_by(ExamRecord.end_time.desc()).all()

    result = []
    for record in records:
        exam = Exam.query.get(record.exam_id)
        user = User.query.get(record.user_id)
        result.append({
            'record': record.to_dict(),
            'exam_name': exam.exam_name if exam else '未知考试',
            'username': user.username if user else '未知用户'
        })

    return jsonify({
        'code': 200,
        'data': result
    })


@bp.route('/wrong_questions', methods=['GET'])
def get_wrong_questions():
    """获取用户的错题列表"""
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400

    wrong_questions = WrongQuestion.query.filter_by(user_id=int(user_id)).order_by(WrongQuestion.add_time.desc()).all()

    result = []
    for wq in wrong_questions:
        question = Question.query.get(wq.question_id)
        if question:
            result.append({
                'wrong_info': wq.to_dict(),
                'question': question.to_dict()
            })

    return jsonify({
        'code': 200,
        'data': result
    })


@bp.route('/questions', methods=['GET'])
def get_questions():
    """获取题库列表"""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    knowledge = request.args.get('knowledge')
    difficulty = request.args.get('difficulty')

    query = Question.query

    if knowledge:
        query = query.filter(Question.knowledge == knowledge)

    if difficulty:
        query = query.filter(Question.difficulty == int(difficulty))

    total = query.count()
    questions = query.order_by(Question.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return jsonify({
        'code': 200,
        'data': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'questions': [q.to_dict() for q in questions]
        }
    })


@bp.route('/question/create', methods=['POST'])
def create_question():
    """创建题目"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    question_text = data.get('question_text', '').strip()
    option_a = data.get('option_a', '').strip()
    option_b = data.get('option_b', '').strip()
    option_c = data.get('option_c', '').strip()
    option_d = data.get('option_d', '').strip()
    answer = data.get('answer', '').strip().upper()

    if not all([question_text, option_a, option_b, option_c, option_d, answer]):
        return jsonify({'code': 400, 'message': '请填写完整题目信息'}), 400

    if answer not in ['A', 'B', 'C', 'D']:
        return jsonify({'code': 400, 'message': '正确答案必须是A/B/C/D'}), 400

    question = Question(
        question_text=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        answer=answer,
        knowledge=data.get('knowledge', ''),
        difficulty=int(data.get('difficulty', 1)),
        score=int(data.get('score', 2)),
        is_ai_generated=int(data.get('is_ai_generated', 0))
    )

    db.session.add(question)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '题目创建成功',
        'data': question.to_dict()
    })


@bp.route('/question/delete/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """删除题目"""
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'code': 404, 'message': '题目不存在'}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '删除成功'
    })
