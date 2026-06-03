# 四川农业大学在线考试系统

基于 Flask 的在线考试系统，支持学生考试、管理员管理、AI错题讲解等功能。

## 技术栈

- **后端**: Flask 3.0 + SQLite
- **前端**: HTML5 + CSS3 + JavaScript
- **数据库**: SQLite（无需额外安装）

## 功能特性

### 学生功能
- 用户注册与登录
- 查看考试列表
- 参加在线考试
- 查看考试成绩
- 错题本与AI讲解

### 管理员功能
- 用户管理
- 题库管理
- 考试管理
- 成绩统计

## 快速开始

### 1. 启动方式

**方式一：双击启动脚本**
```
双击 start.bat 文件
```

**方式二：命令行启动**
```powershell
cd exam_system
.\venv\Scripts\python.exe app.py
```

### 2. 访问系统

打开浏览器访问：http://127.0.0.1:5000

### 3. 登录账号

**管理员账号：**
- 用户名: admin
- 密码: admin123

**学生账号：**
- 注册新账号即可使用

## 项目结构

```
exam_system/
├── app.py              # Flask应用主入口
├── config.py           # 配置文件
├── models.py           # 数据库模型
├── requirements.txt    # 依赖列表
├── start.bat           # 启动脚本
├── api/                # API接口目录
│   ├── __init__.py
│   ├── auth.py         # 登录注册接口
│   ├── exam.py         # 考试相关接口
│   └── ai.py           # AI接口
├── static/             # 静态资源
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript文件
│   └── images/         # 图片资源
└── templates/          # HTML模板
    ├── login.html      # 登录页面
    ├── register.html   # 注册页面
    ├── student/        # 学生端页面
    └── admin/          # 管理员端页面
```

## 初始化数据库

首次运行前请确保已初始化数据库：

```powershell
.\venv\Scripts\python.exe app.py init
```

## 管理员功能说明

1. **用户管理**: 查看和管理所有用户账号
2. **题库管理**: 添加、编辑、删除试题
3. **考试管理**: 创建考试、设置时长、指定试题
4. **成绩统计**: 查看所有考试成绩

## AI功能（预留）

系统预留了AI接口，支持：
- AI错题讲解
- AI自动生成试题
- AI考试总结

配置文件：`ai_config.json`

## 开发说明

### 虚拟环境

虚拟环境已创建在 `venv/` 目录下。

### 依赖安装

```powershell
.\venv\Scripts\pip install -r requirements.txt
```

## 注意事项

1. 确保 Python 3.8+ 版本
2. SQLite数据库文件为 `app.db`，无需额外配置
3. 开发环境已配置调试模式，生产环境请关闭

## License

MIT License