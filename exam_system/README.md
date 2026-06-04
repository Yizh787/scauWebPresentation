# 四川农业大学在线考试系统

基于 Flask 的在线考试系统，支持学生考试、管理员题库/考试/学生管理、AI智能出题与错题讲解等功能。

## 技术栈

- **后端**: Flask 3.0 + SQLAlchemy
- **前端**: HTML5 + CSS3 + JavaScript（原生）
- **数据库**: MySQL（pymysql 驱动）
- **AI**: LangChain + DeepSeek API

## 功能特性

### 学生功能
- 用户注册与登录
- 查看可参加的考试列表
- 参加在线考试（计时、答题、自动判分）
- 查看考试成绩与答题详情
- 错题本与 AI 智能讲解

### 管理员功能

管理后台包含 5 大功能模块：

#### 1. 📝 题库管理
- 查看所有题目列表（题干、知识点、难度、分值）
- 点击「查看/编辑」查看题目详情（题干、ABCD选项、正确答案高亮显示）
- 在线修改题目所有字段并保存
- 删除题目

#### 2. 📋 创建考试
- 输入考试名称、时长
- 从题库中勾选题目组成试卷
- 每道题支持「查看」按钮查看题目详情
- 实时显示已选题目数和总分

#### 3. 🤖 AI 智能出题
- 输入知识点、难度、数量，AI 自动生成选择题
- 生成完成后展示题目列表，每道题可查看/编辑
- 支持勾选/取消题目
- **一键创建考试**：直接输入考试名称和时长，用 AI 生成的题目创建考试
- **加入题库**：题目自动入库，点击关闭即可

#### 4. 📊 考试管理
- 查看所有考试卡片（题目数、总分、时长、创建时间）
- 显示参加人数（已完成/进行中）
- 展开查看每位学生的考试成绩（按分数排序，显示及格/不及格）
- 「查看题目」以只读方式查看考试的所有题目和正确答案
- 删除考试（同步删除关联的考试记录）

#### 5. 👥 学生管理
- 查看所有注册学生列表（用户名、注册时间、已参加考试数）
- 点击「考试记录」查看该学生的所有考试成绩
- 成绩显示分数、总分、及格率（≥60% 绿色，<60% 红色）

## 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 数据库

### 2. 安装依赖

```powershell
cd exam_system
.\venv\Scripts\pip install -r requirements.txt
```

### 3. 配置数据库

编辑 `config.py`，配置 MySQL 连接信息。

### 4. 初始化数据库

```powershell
.\venv\Scripts\python.exe app.py init
```

此命令会创建数据库表并自动生成管理员账号（admin / admin123）。

### 5. 启动系统

**方式一：双击启动脚本**
```
双击 start.bat 文件
```

**方式二：命令行启动**
```powershell
.\venv\Scripts\python.exe app.py
```

### 6. 访问系统

打开浏览器访问：http://127.0.0.1:5000

### 7. 登录账号

**管理员账号：**
- 用户名: `admin`
- 密码: `admin123`

**学生账号：**
- 注册新账号即可使用

## 项目结构

```
exam_system/
├── app.py                  # Flask 应用主入口
├── config.py               # 配置文件（数据库连接等）
├── models.py               # 数据库模型（User, Question, Exam, ExamRecord 等）
├── requirements.txt        # Python 依赖列表
├── start.bat               # Windows 启动脚本
├── start_no_debug.py       # 非调试模式启动
├── init_db.py              # 数据库初始化脚本
├── ai_config.json          # AI API 配置文件
├── api/                    # API 接口目录
│   ├── __init__.py         # 蓝图注册
│   ├── auth.py             # 登录、注册、用户信息接口
│   ├── exam.py             # 考试、题目、学生管理接口
│   └── ai.py               # AI 出题、错题讲解、考试总结接口
├── static/                 # 静态资源
│   ├── css/                # 样式文件
│   ├── js/
│   │   └── api.js          # 前端 API 封装与认证工具
│   └── images/             # 图片资源
└── templates/              # HTML 模板
    ├── login.html           # 登录页
    ├── register.html        # 注册页
    ├── student/             # 学生端页面
    │   ├── student_dashboard.html   # 学生主页
    │   ├── exam.html                # 考试答题页
    │   ├── exam_result.html         # 考试结果页
    │   └── wrong_explain.html       # 错题讲解页
    └── admin/               # 管理员端页面
        └── admin_dashboard.html     # 管理后台（含所有管理功能）
```

## API 接口一览

### 认证相关
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login` | 用户登录 |
| GET | `/api/user/info` | 获取用户信息 |
| POST | `/api/user/update` | 更新用户信息 |

### 题目管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/questions` | 获取题目列表（支持分页、筛选） |
| POST | `/api/question/create` | 创建题目 |
| PUT | `/api/question/update/<id>` | 更新题目 |
| DELETE | `/api/question/delete/<id>` | 删除题目 |

### 考试管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/exams` | 获取考试列表 |
| GET | `/api/exam/<id>` | 获取考试详情（含题目） |
| POST | `/api/exam/create` | 创建考试 |
| DELETE | `/api/exam/<id>/delete` | 删除考试及关联数据 |
| POST | `/api/exam/start` | 开始考试 |
| POST | `/api/exam/submit` | 提交考试 |
| GET | `/api/exam/records` | 获取用户考试记录 |
| GET | `/api/exam/records/all` | 获取所有考试记录（管理员） |
| GET | `/api/exams/manage` | 获取考试管理详情（管理员） |

### 学生管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/students` | 获取所有学生列表（管理员） |
| GET | `/api/wrong_questions` | 获取错题列表 |

### AI 功能
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/ai/config` | 获取 AI 配置状态 |
| POST | `/api/ai/explain` | AI 错题讲解 |
| POST | `/api/ai/generate/questions` | AI 智能出题 |
| POST | `/api/ai/summary` | AI 考试总结 |

## AI 配置

在 `ai_config.json` 中配置 AI API：

```json
{
  "provider": "deepseek",
  "api_key": "your-api-key-here",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat"
}
```

## 数据库模型

- **User**: 用户表（id, username, password, role, avatar, create_time）
- **Question**: 题目表（id, question_text, option_a/b/c/d, answer, knowledge, difficulty, score, is_ai_generated）
- **Exam**: 考试表（id, exam_name, total_score, duration_minutes, create_time）
- **ExamQuestion**: 考试-题目关联表（id, exam_id, question_id, order_num）
- **ExamRecord**: 考试记录表（id, user_id, exam_id, score, total_score, answers_detail, wrong_questions, start_time, end_time）
- **WrongQuestion**: 错题表（id, user_id, question_id, user_answer, ai_explanation, add_time）

## 注意事项

1. 确保 MySQL 服务已启动，并在 `config.py` 中正确配置连接信息
2. 首次运行需执行 `python app.py init` 初始化数据库
3. AI 功能需在 `ai_config.json` 中配置有效的 API Key
4. 开发环境已配置调试模式，生产环境请关闭 debug

## License

MIT License
