"""
AI 接口 - 使用 LangChain 调用大模型
"""
from flask import request, jsonify
from api import bp
from models import db, Question, WrongQuestion
import json
import os
import re

AI_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai_config.json')


def load_ai_config():
    """加载 AI 配置"""
    if os.path.exists(AI_CONFIG_PATH):
        with open(AI_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "provider": "deepseek",
        "api_key": "",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat"
    }


def get_ai_response(prompt, system_prompt=None):
    """调用 AI 接口"""
    config = load_ai_config()

    if not config.get('api_key'):
        return None, "AI API Key 未配置，请先在 ai_config.json 中配置"

    try:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            api_key=config['api_key'],
            base_url=config.get('base_url'),
            model=config.get('model', 'deepseek-chat'),
            temperature=0.7
        )

        if system_prompt:
            from langchain_core.messages import HumanMessage, SystemMessage
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt)
            ]
            response = llm.invoke(messages)
            return response.content, None
        else:
            response = llm.invoke(prompt)
            return response.content, None

    except ImportError as e:
        return None, f"导入 langchain-openai 失败: {e}。请运行: pip install langchain-openai"
    except Exception as e:
        return None, f"AI 调用失败: {str(e)}"


@bp.route('/ai/config', methods=['GET'])
def get_ai_config_status():
    """获取 AI 配置状态"""
    config = load_ai_config()
    api_key = config.get('api_key', '')
    return jsonify({
        'code': 200,
        'data': {
            'provider': config.get('provider', ''),
            'model': config.get('model', ''),
            'base_url': config.get('base_url', ''),
            'configured': bool(api_key),
            'api_key_set': bool(api_key),
            'api_key_preview': api_key[:8] + '****' + api_key[-4:] if len(api_key) > 12 else ('****' if api_key else '')
        }
    })


@bp.route('/ai/config/save', methods=['POST'])
def save_ai_config():
    """保存 AI 配置（先测试连接）"""
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    provider = data.get('provider', '').strip()
    api_key = data.get('api_key', '').strip()
    base_url = data.get('base_url', '').strip()
    model = data.get('model', '').strip()

    if not all([provider, api_key, base_url, model]):
        return jsonify({'code': 400, 'message': '所有字段均为必填'}), 400

    # 测试连接
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0.7,
            timeout=15
        )
        response = llm.invoke([HumanMessage(content='你好，请回复"连接成功"')])
        if not response or not response.content:
            return jsonify({'code': 500, 'message': 'AI 服务返回为空，请检查配置'}), 500
    except ImportError:
        return jsonify({'code': 500, 'message': 'langchain-openai 未安装，请运行: pip install langchain-openai'}), 500
    except Exception as e:
        error_msg = str(e)
        if 'auth' in error_msg.lower() or 'key' in error_msg.lower() or '401' in error_msg:
            return jsonify({'code': 500, 'message': '连接失败：API Key 无效'}), 500
        elif 'timeout' in error_msg.lower() or 'connect' in error_msg.lower():
            return jsonify({'code': 500, 'message': '连接失败：无法连接到服务器，请检查 Base URL'}), 500
        elif 'model' in error_msg.lower() or '404' in error_msg:
            return jsonify({'code': 500, 'message': '连接失败：模型名称无效'}), 500
        return jsonify({'code': 500, 'message': f'连接失败：{error_msg}'}), 500

    # 连接成功，保存配置
    config = {
        'provider': provider,
        'api_key': api_key,
        'base_url': base_url,
        'model': model,
        'temperature': 0.7
    }
    try:
        with open(AI_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return jsonify({'code': 500, 'message': f'保存配置文件失败：{str(e)}'}), 500

    return jsonify({
        'code': 200,
        'message': '连接成功，配置已保存',
        'data': {
            'provider': provider,
            'model': model,
            'base_url': base_url,
            'api_key_preview': api_key[:8] + '****' + api_key[-4:] if len(api_key) > 12 else '****'
        }
    })


@bp.route('/ai/config/test', methods=['POST'])
def test_ai_connection():
    """测试 AI 连接（不保存）"""
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    api_key = data.get('api_key', '').strip()
    base_url = data.get('base_url', '').strip()
    model = data.get('model', '').strip()

    if not all([api_key, base_url, model]):
        return jsonify({'code': 400, 'message': 'API Key、Base URL、模型名均为必填'}), 400

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0.7,
            timeout=15
        )
        response = llm.invoke([HumanMessage(content='你好，请回复"连接成功"')])
        if not response or not response.content:
            return jsonify({'code': 500, 'message': 'AI 服务返回为空，请检查配置'}), 500
    except ImportError:
        return jsonify({'code': 500, 'message': 'langchain-openai 未安装，请运行: pip install langchain-openai'}), 500
    except Exception as e:
        error_msg = str(e)
        if 'auth' in error_msg.lower() or 'key' in error_msg.lower() or '401' in error_msg:
            return jsonify({'code': 500, 'message': '连接失败：API Key 无效'}), 500
        elif 'timeout' in error_msg.lower() or 'connect' in error_msg.lower():
            return jsonify({'code': 500, 'message': '连接失败：无法连接到服务器，请检查 Base URL'}), 500
        elif 'model' in error_msg.lower() or '404' in error_msg:
            return jsonify({'code': 500, 'message': '连接失败：模型名称无效'}), 500
        return jsonify({'code': 500, 'message': f'连接失败：{error_msg}'}), 500

    return jsonify({
        'code': 200,
        'message': '连接成功',
        'data': {
            'response': response.content[:100] if response.content else ''
        }
    })


@bp.route('/ai/explain', methods=['POST'])
def ai_explain():
    """AI 讲解错题"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    question_id = data.get('question_id')

    if not question_id:
        return jsonify({'code': 400, 'message': '题目ID不能为空'}), 400

    question = Question.query.get(int(question_id))
    if not question:
        return jsonify({'code': 404, 'message': '题目不存在'}), 404

    user_answer = data.get('user_answer', '')

    system_prompt = """你是一位专业的教育助手，专门帮助学生理解错题。请：
1. 解释正确答案为什么是正确的
2. 分析学生可能选错的原因
3. 提供解题思路和知识点总结
4. 用简洁易懂的语言解释"""

    prompt = f"""题目：{question.question_text}

选项：
A. {question.option_a}
B. {question.option_b}
C. {question.option_c}
D. {question.option_d}

正确答案：{question.answer}
学生答案：{user_answer if user_answer else '未作答'}

知识点：{question.knowledge if question.knowledge else '未标注'}

请给出详细的讲解。"""

    explanation, error = get_ai_response(prompt, system_prompt)

    if error:
        return jsonify({'code': 500, 'message': error}), 500

    wrong_q = WrongQuestion.query.filter_by(user_id=data.get('user_id'), question_id=question_id).first()
    if wrong_q:
        wrong_q.ai_explanation = explanation
        db.session.commit()

    return jsonify({
        'code': 200,
        'data': {
            'explanation': explanation,
            'question': question.to_dict()
        }
    })


@bp.route('/ai/generate/questions', methods=['POST'])
def ai_generate_questions():
    """AI 生成题目"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    knowledge = data.get('knowledge', '')
    difficulty = data.get('difficulty', 2)
    count = min(int(data.get('count', 5)), 10)

    system_prompt = """你是一位专业的出题老师，请根据用户需求生成高质量的选择题。
要求：
1. 题目清晰明了，不能有歧义
2. 选项之间区分度明显
3. 正确答案必须唯一
4. 知识点覆盖准确

请以 JSON 格式返回，格式如下：
{{
  "questions": [
    {{
      "question_text": "题目内容",
      "option_a": "A选项内容",
      "option_b": "B选项内容",
      "option_c": "C选项内容",
      "option_d": "D选项内容",
      "answer": "正确答案字母",
      "knowledge": "知识点",
      "difficulty": 难度等级(1-3),
      "score": 分值
    }}
  ]
}}"""

    difficulty_text = {1: "简单", 2: "中等", 3: "困难"}
    prompt = f"""请生成 {count} 道 {difficulty_text.get(difficulty, '中等')} 难度、知识点为「{knowledge if knowledge else '计算机基础'}」的选择题。"""

    response_text, error = get_ai_response(prompt, system_prompt)

    if error:
        return jsonify({'code': 500, 'message': error}), 500

    try:
        cleaned = re.sub(r'```(?:json)?\s*', '', response_text).strip().rstrip('`').strip()
        result = json.loads(cleaned)
        questions = result.get('questions', [])

        saved_questions = []
        for q in questions:
            question = Question(
                question_text=q.get('question_text', ''),
                option_a=q.get('option_a', ''),
                option_b=q.get('option_b', ''),
                option_c=q.get('option_c', ''),
                option_d=q.get('option_d', ''),
                answer=q.get('answer', 'A').upper(),
                knowledge=q.get('knowledge', knowledge),
                difficulty=int(q.get('difficulty', difficulty)),
                score=int(q.get('score', 2)),
                is_ai_generated=1
            )
            db.session.add(question)
            saved_questions.append(question)

        db.session.commit()

        return jsonify({
            'code': 200,
            'message': f'成功生成 {len(saved_questions)} 道题目',
            'data': [q.to_dict() for q in saved_questions]
        })

    except json.JSONDecodeError:
        return jsonify({'code': 500, 'message': 'AI 返回格式错误，无法解析'}), 500


@bp.route('/ai/summary', methods=['POST'])
def ai_summary():
    """AI 生成考试总结"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求数据格式错误'}), 400

    record_id = data.get('record_id')

    if not record_id:
        return jsonify({'code': 400, 'message': '考试记录ID不能为空'}), 400

    from models import ExamRecord, Exam
    record = ExamRecord.query.get(int(record_id))
    if not record:
        return jsonify({'code': 404, 'message': '考试记录不存在'}), 404

    exam = Exam.query.get(record.exam_id)
    wrong_ids = json.loads(record.wrong_questions) if record.wrong_questions else []

    wrong_questions_list = []
    for wq_id in wrong_ids:
        question = Question.query.get(wq_id)
        if question:
            wrong_questions_list.append(question.to_dict())

    system_prompt = """你是一位专业的学习顾问，请根据学生的考试表现提供个性化的学习建议。"""

    score_rate = record.score / record.total_score if record.total_score > 0 else 0
    score_text = "优秀" if score_rate >= 0.9 else "良好" if score_rate >= 0.7 else "一般" if score_rate >= 0.6 else "较差"

    prompt = f"""学生考试成绩分析：
- 考试名称：{exam.exam_name if exam else '未知'}
- 得分：{record.score}/{record.total_score}
- 正确率：{score_rate*100:.1f}%
- 表现评价：{score_text}

错题数量：{len(wrong_questions_list)} 道

请提供：
1. 本次考试的整体评价
2. 知识点薄弱环节分析
3. 针对性的学习建议
4. 后续学习计划建议"""

    summary, error = get_ai_response(prompt, system_prompt)

    if error:
        return jsonify({'code': 500, 'message': error}), 500

    return jsonify({
        'code': 200,
        'data': {
            'summary': summary,
            'score': record.score,
            'total_score': record.total_score,
            'wrong_count': len(wrong_questions_list)
        }
    })
