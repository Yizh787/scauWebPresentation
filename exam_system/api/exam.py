"""
考试相关接口
"""
from flask import request, jsonify
from api import bp
from models import db, Exam, ExamQuestion, ExamRecord, Question, WrongQuestion, User
from datetime import datetime
import json
import random


@bp.route('/students', methods=['GET'])
def get_students():
    """获取所有学生列表（管理员）- 优化版"""
    from sqlalchemy import func

    students = User.query.filter_by(role=0).order_by(User.create_time.desc()).all()
    if not students:
        return jsonify({'code': 200, 'data': []})

    student_ids = [s.id for s in students]

    # 批量查询每个学生的已完成考试数量
    exam_counts = dict(
        db.session.query(ExamRecord.user_id, func.count(ExamRecord.id))
        .filter(ExamRecord.user_id.in_(student_ids), ExamRecord.end_time.isnot(None))
        .group_by(ExamRecord.user_id)
        .all()
    )

    result = []
    for s in students:
        result.append({
            'id': s.id,
            'username': s.username,
            'create_time': s.create_time.strftime('%Y-%m-%d %H:%M:%S') if s.create_time else None,
            'exam_count': exam_counts.get(s.id, 0)
        })

    return jsonify({
        'code': 200,
        'data': result
    })


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
    """获取考试详情（含题目），支持乱序防作弊"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'code': 404, 'message': '考试不存在'}), 404

    record_id = request.args.get('record_id')

    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(ExamQuestion.order_num).all()

    questions = []
    for eq in exam_questions:
        question = Question.query.get(eq.question_id)
        if question:
            questions.append(question.to_dict())

    # 如果传入 record_id，按乱序返回
    if record_id:
        record = ExamRecord.query.get(int(record_id))
        if record and record.shuffle_data:
            shuffle_info = json.loads(record.shuffle_data)
            q_order = shuffle_info['question_order']
            opt_maps = shuffle_info['option_maps']

            # 按乱序排列题目
            q_map = {q['id']: q for q in questions}
            shuffled_questions = []
            for qid in q_order:
                if qid not in q_map:
                    continue
                q = q_map[qid].copy()
                opt_map = opt_maps[str(qid)]
                # 按乱序重排选项内容
                orig = {
                    'A': q['option_a'], 'B': q['option_b'],
                    'C': q['option_c'], 'D': q['option_d']
                }
                q['option_a'] = orig[opt_map['A']]
                q['option_b'] = orig[opt_map['B']]
                q['option_c'] = orig[opt_map['C']]
                q['option_d'] = orig[opt_map['D']]
                # answer 也映射为乱序后的标签
                orig_answer = q['answer']
                # 找到 orig_answer 在 opt_map 中被映射到哪个 shuffled label
                for shuffled_label, original_label in opt_map.items():
                    if original_label == orig_answer:
                        q['answer'] = shuffled_label
                        break
                shuffled_questions.append(q)
            questions = shuffled_questions

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
    shuffle_enabled = int(data.get('shuffle_enabled', 0))

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
        total_score=total_score,
        shuffle_enabled=shuffle_enabled
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

    # 生成防作弊乱序数据（仅在开启乱序时）
    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).all()
    question_ids = [eq.question_id for eq in exam_questions]

    shuffle_data = None
    if exam.shuffle_enabled:
        # 题目乱序
        shuffled_ids = question_ids[:]
        random.shuffle(shuffled_ids)

        # 选项乱序：每道题的 ABCD 随机打乱
        original_labels = ['A', 'B', 'C', 'D']
        option_maps = {}  # { question_id: { shuffled_label: original_label } }
        for qid in question_ids:
            perm = original_labels[:]
            random.shuffle(perm)
            option_maps[str(qid)] = {perm[i]: original_labels[i] for i in range(4)}

        shuffle_data = json.dumps({
            'question_order': shuffled_ids,
            'option_maps': option_maps
        }, ensure_ascii=False)

    record = ExamRecord(
        user_id=user_id,
        exam_id=exam_id,
        total_score=exam.total_score,
        shuffle_data=shuffle_data,
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

    # 加载乱序映射
    # opt_map 的含义: {shuffled_label: original_label}
    # 例如 {'A': 'B', 'B': 'D', 'C': 'A', 'D': 'C'}
    # 表示：显示的A位置放的是原始B的内容
    opt_maps = {}
    if record.shuffle_data:
        shuffle_info = json.loads(record.shuffle_data)
        opt_maps = shuffle_info.get('option_maps', {})

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

        # 将学生的乱序答案还原为原始答案
        # 学生选的是显示的标签（如A），需要找到显示的A对应的是哪个原始选项
        original_answer = user_answer
        if user_answer and str(question.id) in opt_maps:
            # opt_map 直接就是 {shuffled_label: original_label}
            original_answer = opt_maps[str(question.id)].get(user_answer.upper(), user_answer)

        if original_answer and original_answer.upper() == question.answer.upper():
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


@bp.route('/exams/manage', methods=['GET'])
def get_exams_manage():
    """获取所有考试及参与情况（管理员）- 优化版"""
    from sqlalchemy import func

    # 一次性查询所有考试
    exams = Exam.query.order_by(Exam.create_time.desc()).all()
    if not exams:
        return jsonify({'code': 200, 'data': []})

    exam_ids = [e.id for e in exams]

    # 批量查询每个考试的题目数量
    question_counts = dict(
        db.session.query(ExamQuestion.exam_id, func.count(ExamQuestion.id))
        .filter(ExamQuestion.exam_id.in_(exam_ids))
        .group_by(ExamQuestion.exam_id)
        .all()
    )

    # 批量查询所有考试记录
    all_records = ExamRecord.query.filter(ExamRecord.exam_id.in_(exam_ids)).all()

    # 按 exam_id 分组记录
    records_by_exam = {}
    for r in all_records:
        if r.exam_id not in records_by_exam:
            records_by_exam[r.exam_id] = []
        records_by_exam[r.exam_id].append(r)

    # 批量查询所有相关用户
    user_ids = list(set(r.user_id for r in all_records if r.end_time is not None))
    users_map = {}
    if user_ids:
        users = User.query.filter(User.id.in_(user_ids)).all()
        users_map = {u.id: u for u in users}

    result = []
    for exam in exams:
        records = records_by_exam.get(exam.id, [])
        completed = [r for r in records if r.end_time is not None]
        in_progress = [r for r in records if r.end_time is None]

        participants = []
        for r in completed:
            user = users_map.get(r.user_id)
            participants.append({
                'username': user.username if user else '未知用户',
                'score': r.score,
                'total_score': r.total_score,
                'end_time': r.end_time.strftime('%Y-%m-%d %H:%M:%S') if r.end_time else None
            })

        result.append({
            'exam': exam.to_dict(),
            'question_count': question_counts.get(exam.id, 0),
            'completed_count': len(completed),
            'in_progress_count': len(in_progress),
            'participants': participants
        })

    return jsonify({
        'code': 200,
        'data': result
    })


@bp.route('/exam/<int:exam_id>/delete', methods=['DELETE'])
def delete_exam(exam_id):
    """删除考试及其关联数据（管理员）"""
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'code': 404, 'message': '考试不存在'}), 404

    # 删除关联的考试题目
    ExamQuestion.query.filter_by(exam_id=exam_id).delete()
    # 删除关联的考试记录
    ExamRecord.query.filter_by(exam_id=exam_id).delete()
    # 删除考试
    db.session.delete(exam)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '考试已删除'
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


@bp.route('/question/update/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """更新题目（管理员）"""
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'code': 404, 'message': '题目不存在'}), 404

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

    question.question_text = question_text
    question.option_a = option_a
    question.option_b = option_b
    question.option_c = option_c
    question.option_d = option_d
    question.answer = answer
    question.knowledge = data.get('knowledge', '')
    question.difficulty = int(data.get('difficulty', 1))
    question.score = int(data.get('score', 2))

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '更新成功',
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
