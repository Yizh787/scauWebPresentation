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

### 智能防作弊系统（可选开启）
- **管理员可控**：创建考试时可选择是否开启乱序模式
- **题目乱序**：开启后每位考生看到的题目顺序随机打乱，每人不同
- **选项乱序**：ABCD 选项位置随机排列，答案映射存储在数据库中
- **提交还原**：学生提交答案时，系统自动将乱序答案还原为原始答案进行判分
- **管理员无感**：管理员查看考试题目时仍显示原始顺序和选项

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
- **ExamRecord**: 考试记录表（id, user_id, exam_id, score, total_score, answers_detail, wrong_questions, shuffle_data, start_time, end_time）
- **WrongQuestion**: 错题表（id, user_id, question_id, user_answer, ai_explanation, add_time）

## 注意事项

1. 确保 MySQL 服务已启动，并在 `config.py` 中正确配置连接信息
2. 首次运行需执行 `python app.py init` 初始化数据库
3. AI 功能需在 `ai_config.json` 中配置有效的 API Key
4. 开发环境已配置调试模式，生产环境请关闭 debug

## 功能模块详细说明

### 一、学生功能模块

#### 1. 用户注册与登录
- **注册功能**：学生可以通过注册页面创建账号
  - 设置用户名（至少4位字符）
  - 设置密码（至少6位字符）
  - 系统自动分配学生角色（role=0）
- **登录功能**：学生使用用户名和密码登录系统
  - 登录成功后自动跳转至学生主页
  - 登录状态通过 localStorage 持久化保存
  - 支持自动识别角色并跳转对应页面

#### 2. 考试列表查看
- 学生登录后可查看所有可参加的考试
- 已完成的考试不会显示在列表中
- 显示考试名称、时长、总分等基本信息
- 点击可直接进入考试页面

#### 3. 在线考试答题
- **计时功能**：考试开始后自动倒计时
- **题目展示**：按顺序展示题目，支持乱序模式（管理员配置）
- **答题方式**：点击选项选择答案，支持单选
- **进度显示**：实时显示已答题目数和总题目数
- **防作弊机制**：
  - 题目顺序乱序（每位考生不同）
  - 选项顺序乱序（ABCD位置随机）
  - 系统自动还原答案进行判分

#### 4. 考试结果查看
- 考试提交后立即显示成绩
- 展示得分、总分、正确率
- 显示及格状态（≥60分为及格，显示绿色；<60分为不及格，显示红色）
- 可查看每道题的答题详情和正确答案

#### 5. 错题本与AI讲解
- **错题收集**：系统自动收集学生做错的题目
- **错题列表**：按时间倒序显示错题记录
- **AI讲解**：点击可获取AI生成的题目解析和讲解
- **知识点关联**：显示题目所属知识点和难度等级

---

### 二、管理员功能模块

#### 1. 📝 题库管理
- **题目列表查看**：分页显示所有题目
  - 显示题干摘要、知识点、难度、分值
  - 支持按知识点和难度筛选
- **题目详情查看**：点击查看完整题目信息
  - 显示完整题干和四个选项
  - 正确答案高亮显示（绿色背景）
- **题目编辑**：在线修改题目所有字段
  - 修改题干、选项A/B/C/D
  - 修改正确答案、知识点、难度、分值
  - 保存后立即生效
- **题目删除**：支持删除单道题目
  - 系统自动删除关联的错题记录

#### 2. 📋 创建考试
- **考试基本信息设置**：
  - 输入考试名称（必填）
  - 设置考试时长（分钟）
  - 选择是否开启乱序模式（防作弊）
- **题目选择**：
  - 从题库中勾选题目组成试卷
  - 支持搜索和筛选题目
  - 每道题可点击查看详情
  - 实时显示已选题目数和总分
- **考试创建**：点击保存后生成考试

#### 3. 🤖 AI 智能出题
- **参数设置**：
  - 输入知识点（如：数据结构、算法、数据库）
  - 选择难度等级（1-简单、2-中等、3-困难）
  - 设置生成题目数量（1-20道）
- **生成过程**：
  - 点击生成按钮后显示进度条
  - AI自动生成符合要求的选择题
- **题目审核**：
  - 生成完成后展示题目列表
  - 每道题可查看详情和编辑
  - 支持勾选/取消题目
- **快速操作**：
  - **一键创建考试**：直接用AI生成的题目创建考试
  - **加入题库**：题目自动入库，不创建考试

#### 4. 📊 考试管理
- **考试列表**：以卡片形式展示所有考试
  - 显示考试名称、题目数、总分、时长、创建时间
  - 显示参加人数（已完成/进行中）
- **考试详情**：
  - 展开查看每位学生的考试成绩
  - 按分数排序显示
  - 及格状态可视化（绿色/红色标识）
- **题目预览**：以只读方式查看考试的所有题目和正确答案
- **考试删除**：删除考试及其所有关联数据（考试题目、考试记录）

#### 5. 👥 学生管理
- **学生列表**：显示所有注册学生
  - 用户名、注册时间、已参加考试数
- **学生详情**：
  - 点击"考试记录"查看该学生的所有考试成绩
  - 显示每次考试的分数、总分、及格率
  - 及格率可视化（≥60%绿色，<60%红色）

---

### 三、智能防作弊系统

#### 功能特性
- **管理员可控**：创建考试时可选择是否开启乱序模式
- **题目乱序**：开启后每位考生看到的题目顺序随机打乱，每人不同
- **选项乱序**：ABCD选项位置随机排列，答案映射存储在数据库中
- **提交还原**：学生提交答案时，系统自动将乱序答案还原为原始答案进行判分
- **管理员无感**：管理员查看考试题目时仍显示原始顺序和选项

#### 实现机制
- **乱序数据存储**：每次考试开始时生成乱序映射数据（JSON格式）
- **题目顺序映射**：记录题目ID的随机排列顺序
- **选项映射表**：记录每道题的选项位置映射关系
- **答案还原算法**：提交时根据映射表还原学生答案

---

### 四、AI 功能模块

#### 1. AI 配置管理
- **配置项**：
  - 服务商选择（当前支持DeepSeek）
  - API Key 设置
  - Base URL 配置
  - 模型选择
- **配置验证**：支持测试连接功能
- **配置状态**：显示当前配置状态（已配置/未配置）

#### 2. AI 智能出题
- 根据知识点和难度自动生成选择题
- 生成的题目包含题干、四个选项和正确答案
- 自动标记为AI生成（is_ai_generated=1）

#### 3. AI 错题讲解
- 针对学生做错的题目生成详细讲解
- 包括题目分析、正确答案解析、知识点扩展

#### 4. AI 考试总结
- 针对学生的考试表现生成总结报告
- 分析强项和弱项知识点
- 提供学习建议

---

### 五、数据库模型详细说明

#### 1. User（用户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 用户唯一标识（自增主键） |
| username | String(50) | 用户名（唯一） |
| password | String(255) | 密码（SHA256哈希） |
| role | SmallInteger | 角色（0=学生，1=管理员） |
| avatar | String(255) | 头像URL（可选） |
| create_time | DateTime | 创建时间 |

#### 2. Question（题目表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 题目唯一标识（自增主键） |
| question_text | Text | 题干内容 |
| option_a | String(255) | 选项A内容 |
| option_b | String(255) | 选项B内容 |
| option_c | String(255) | 选项C内容 |
| option_d | String(255) | 选项D内容 |
| answer | String(1) | 正确答案（A/B/C/D） |
| knowledge | String(100) | 所属知识点 |
| difficulty | SmallInteger | 难度等级（1/2/3） |
| score | Integer | 分值（默认2分） |
| is_ai_generated | SmallInteger | 是否AI生成（0/1） |
| create_time | DateTime | 创建时间 |

#### 3. Exam（考试表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 考试唯一标识（自增主键） |
| exam_name | String(100) | 考试名称 |
| total_score | Integer | 总分 |
| duration_minutes | Integer | 考试时长（分钟） |
| shuffle_enabled | SmallInteger | 是否开启乱序（0/1） |
| create_time | DateTime | 创建时间 |

#### 4. ExamQuestion（考试-题目关联表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 关联记录唯一标识 |
| exam_id | Integer | 关联考试ID |
| question_id | Integer | 关联题目ID |
| order_num | Integer | 题目在考试中的顺序 |

#### 5. ExamRecord（考试记录表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 记录唯一标识（自增主键） |
| user_id | Integer | 考生ID |
| exam_id | Integer | 考试ID |
| score | Integer | 得分 |
| total_score | Integer | 总分 |
| answers_detail | Text | 答题详情（JSON） |
| wrong_questions | Text | 错题列表（JSON） |
| shuffle_data | Text | 乱序数据（JSON） |
| start_time | DateTime | 开始时间 |
| end_time | DateTime | 结束时间 |

#### 6. WrongQuestion（错题表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 记录唯一标识（自增主键） |
| user_id | Integer | 学生ID |
| question_id | Integer | 错题ID |
| user_answer | String(1) | 学生答案 |
| ai_explanation | Text | AI讲解内容 |
| add_time | DateTime | 添加时间 |

---

### 六、配置说明

#### 1. 数据库配置（config.py）
```python
# MySQL 数据库连接配置
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'exam_system'

# Flask 配置
SECRET_KEY = 'your_secret_key'
DEBUG = True  # 生产环境请设为 False
```

#### 2. AI 配置（ai_config.json）
```json
{
  "provider": "deepseek",
  "api_key": "your-api-key-here",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat"
}
```

---

## License

MIT License
