# 四川农业大学在线考试系统

基于 Flask 的在线考试系统，支持学生考试、管理员题库/考试/学生管理、AI智能出题与错题讲解等功能。

## 技术栈

- **后端**: Flask 3.0 + SQLAlchemy
- **前端**: HTML5 + CSS3 + JavaScript（原生）
- **数据库**: SQLite（开发）/ MySQL（生产）
- **AI**: LangChain + DeepSeek API

## 功能特性

### 学生功能

#### 📋 试卷中心
- 查看可参加的考试列表
- 显示考试时长、总分信息
- 一键开始考试

#### 📊 考试记录
- 查看所有历史考试成绩
- 显示分数、及格率统计
- 支持查看答题详情

#### 📝 错题本
- 自动收集考试错题
- AI 智能讲解错题
- 知识点分类整理

#### 🎯 考试界面
- 倒计时提醒（最后5分钟警告）
- 答案自动保存（防止意外丢失）
- 进度条显示答题进度
- 交卷确认弹窗

### 智能防作弊系统

管理员创建考试时可选择是否开启乱序模式：

- **题目乱序**：每位考生看到的题目顺序随机打乱
- **选项乱序**：ABCD 选项位置随机排列
- **答案映射**：系统自动存储映射关系，提交时自动还原
- **管理员无感**：管理员查看题目时仍显示原始顺序

### 管理员功能

管理后台采用**左侧标签导航 + 右侧内容区**布局，包含 5 大功能模块：

#### 📊 数据概览
- 统计卡片：题库总数、考试场次、学生人数、AI状态
- 难度分布图：可视化题目难度分布
- 最近考试：快速查看最新考试情况

#### 📝 题库管理
- 题目列表：表格展示所有题目（ID、题干、知识点、难度、分值）
- 搜索过滤：支持关键词搜索和难度筛选
- 添加题目：内联表单，无需弹窗
- 编辑题目：点击编辑打开模态框，显示选项预览和正确答案
- 删除题目：二次确认后删除

#### 📋 考试管理
- 考试卡片：展示考试详情（题目数、总分、时长、乱序状态）
- 参与统计：显示参加人数、完成人数
- 成绩排名：前5名学生成绩预览
- **创建考试**：
  - 输入考试名称、时长
  - 选择是否开启乱序
  - 从题库勾选题目
  - **题目预览**：点击预览按钮查看完整题目、选项、正确答案
- **查看题目**：以只读方式查看考试的所有题目和正确答案
- 删除考试：同步删除关联的考试记录

#### 👥 学生管理
- 学生列表：展示所有注册学生
- 搜索功能：按用户名搜索
- 考试记录：查看每位学生的所有考试成绩

#### 🤖 AI 智能出题
- 输入知识点、难度、数量
- **进度条动画**：实时显示生成进度
- 生成结果展示：题目列表可预览
- 一键创建考试：直接用 AI 生成的题目创建考试

## 快速开始

### 1. 环境要求

- Python 3.8+
- SQLite（开发）或 MySQL（生产）

### 2. 安装依赖

```bash
cd exam_system
pip install -r requirements.txt
```

### 3. 配置数据库

开发环境使用 SQLite，无需额外配置。

生产环境请编辑 `config.py`，配置 MySQL 连接信息。

### 4. 初始化数据库

```bash
cd exam_system
python app.py init
```

此命令会创建数据库表并自动生成管理员账号（admin / admin123）。

### 5. 启动系统

**方式一：双击启动脚本**
```
双击 start.bat 文件
```

**方式二：命令行启动**
```bash
python app.py
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
scauWebPresentation/
├── README.md                    # 项目说明（本文件）
├── exam_system/                 # 主项目目录
│   ├── app.py                   # Flask 应用主入口
│   ├── config.py                # 配置文件（数据库连接等）
│   ├── models.py                # 数据库模型
│   ├── requirements.txt         # Python 依赖列表
│   ├── start.bat                # Windows 启动脚本
│   ├── start_no_debug.py        # 非调试模式启动
│   ├── init_db.py               # 数据库初始化脚本
│   ├── ai_config.json           # AI API 配置文件
│   ├── api/                     # API 接口目录
│   │   ├── __init__.py          # 蓝图注册
│   │   ├── auth.py              # 登录、注册、用户信息接口
│   │   ├── exam.py              # 考试、题目、学生管理接口
│   │   └── ai.py                # AI 出题、错题讲解接口
│   ├── static/                  # 静态资源
│   │   ├── css/
│   │   │   ├── style.css        # 全局样式
│   │   │   ├── student.css      # 学生端样式
│   │   │   └── admin.css        # 管理员端样式
│   │   ├── js/
│   │   │   └── api.js           # 前端 API 封装与认证工具
│   │   └── images/              # 图片资源
│   └── templates/               # HTML 模板
│       ├── login.html           # 登录页
│       ├── register.html        # 注册页
│       ├── student/             # 学生端页面
│       │   ├── student_dashboard.html   # 学生主页
│       │   ├── exam.html                # 考试答题页
│       │   ├── exam_result.html         # 考试结果页
│       │   └── wrong_explain.html       # 错题讲解页
│       └── admin/               # 管理员端页面
│           └── admin_dashboard.html     # 管理后台
```

## 数据库模型

| 模型 | 说明 | 主要字段 |
|------|------|----------|
| User | 用户表 | id, username, password, role, avatar, create_time |
| Question | 题目表 | id, question_text, option_a/b/c/d, answer, knowledge, difficulty, score |
| Exam | 考试表 | id, exam_name, total_score, duration_minutes, shuffle_enabled |
| ExamQuestion | 考试-题目关联 | id, exam_id, question_id, order_num |
| ExamRecord | 考试记录 | id, user_id, exam_id, score, total_score, shuffle_data, start_time, end_time |
| WrongQuestion | 错题表 | id, user_id, question_id, user_answer, ai_explanation |

## API 接口

### 认证相关
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login` | 用户登录 |
| GET | `/api/user/info` | 获取用户信息 |

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
| GET | `/api/exam/<id>` | 获取考试详情（含题目，支持乱序） |
| POST | `/api/exam/create` | 创建考试 |
| DELETE | `/api/exam/<id>/delete` | 删除考试及关联数据 |
| POST | `/api/exam/start` | 开始考试（生成乱序数据） |
| POST | `/api/exam/submit` | 提交考试（自动还原乱序答案） |
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

在 `exam_system/ai_config.json` 中配置 AI API：

```json
{
  "provider": "deepseek",
  "api_key": "your-api-key-here",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat"
}
```

## 设计规范

### 色彩系统（Forest Palette）

| 颜色 | 色值 | 用途 |
|------|------|------|
| Forest | #1a5c1a | 深绿，标题、强调 |
| Canopy | #2d8a2d | 主绿，按钮、链接 |
| Sprout | #3da33d | 浅绿，渐变终点 |
| Error | #e74c3c | 错误状态 |
| Success | #27ae60 | 成功状态 |
| Warning | #f39c12 | 警告状态 |

### 字体

使用系统字体栈，支持中英文：
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 
             'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
```

### 圆角

- 卡片：12px
- 按钮：8px
- 输入框：8px
- 标签：4px

## 更新日志

### v2.0 (2026-06-07)

**管理后台重构**
- 从模态框布局改为左侧标签导航 + 右侧内容区布局
- 新增数据概览面板（统计卡片、难度分布图、最近考试）
- 题库管理改为内联表格，支持搜索过滤
- 考试管理改为卡片列表，内联创建表单
- AI 出题增加进度条动画

**学生端改进**
- 试卷中心和考试记录分开展示
- 记录页面显示全部历史成绩
- 标题随 tab 切换动态更新

**Bug 修复**
- 修复乱序模式下答案映射错误的问题
- 修复考试管理点击查看题目无反应的问题

**新功能**
- 创建考试时支持题目预览（显示选项和正确答案）

### v1.0 (2026-06-01)

- 初始版本发布
- 学生考试、管理员后台、AI 出题等核心功能

## License

MIT License
