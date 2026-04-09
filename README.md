## 项目描述

这是一个基于Flask框架开发的个人网站，包含文件上传、用户管理、信息收集、社区留言等功能。网站采用现代化的设计风格，支持响应式布局，可在不同设备上正常显示。

## 功能特点

- **文件上传**：支持多种文件类型的上传，包括图片、音频、视频等
- **用户管理**：支持用户注册、登录，以及管理员审核注册申请
- **信息收集**：可自定义表单字段，收集用户信息并导出为Excel文件
- **社区留言**：已登录用户可以在社区页面发布留言
- **数据持久化**：所有数据存储在JSON文件中，确保应用重启后数据不丢失
- **管理员功能**：管理员可以审核注册申请、删除上传的文件等

## 技术栈

- **后端**：Python 3.x, Flask 2.0.1
- **前端**：HTML5, CSS3, JavaScript
- **数据存储**：JSON文件
- **依赖管理**：pip

## 部署指南

### 本地开发

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   - 复制 `.env.example` 文件为 `.env`
   - 填写 `SECRET_KEY` 和 `ADMIN_PASSWORD` 等配置

4. **启动应用**
   ```bash
   python app.py
   ```

5. **访问网站**
   打开浏览器，访问 `http://localhost:5000`

### 部署到GitHub Pages

由于GitHub Pages主要用于静态网站，本项目作为动态Flask应用，需要部署到支持Python的云平台，如Heroku、Vercel、Render等。

### 部署到Heroku

1. **创建Heroku账户**
   访问 [Heroku官网](https://www.heroku.com/) 注册账户

2. **安装Heroku CLI**
   按照官方文档安装Heroku命令行工具

3. **登录Heroku**
   ```bash
   heroku login
   ```

4. **创建Heroku应用**
   ```bash
   heroku create <app-name>
   ```

5. **配置环境变量**
   ```bash
   heroku config:set SECRET_KEY=your_secret_key_here
   heroku config:set ADMIN_PASSWORD=your_admin_password_here
   ```

6. **部署应用**
   ```bash
   git push heroku main
   ```

7. **启动应用**
   ```bash
   heroku ps:scale web=1
   ```

8. **访问应用**
   运行 `heroku open` 打开应用

## 项目结构

```
.
├── app.py              # 应用主文件
├── Procfile            # Heroku部署配置
├── requirements.txt    # 依赖文件
├── .env.example        # 环境变量示例
├── README.md           # 项目说明
├── uploads/            # 上传文件存储目录
├── data/               # 数据文件存储目录
└── templates/          # HTML模板目录
    ├── index.html      # 首页
    ├── login.html      # 登录页面
    ├── community.html  # 社区页面
    ├── info_collect.html  # 信息收集页面
    ├── edit_info_form.html  # 编辑表单页面
    ├── view_user_data.html  # 查看用户数据页面
    ├── review_registration.html  # 审核注册页面
    └── success.html    # 成功页面
```

## 管理员账户

默认管理员账户：
- 用户名：admin
- 密码：admin123（可在.env文件中修改）

## 注意事项

1. **文件存储**：上传的文件存储在 `uploads` 目录中，请确保该目录有足够的存储空间
2. **数据安全**：敏感信息（如SECRET_KEY）应通过环境变量配置，不要直接硬编码在代码中
3. **部署环境**：在生产环境中，应将 `FLASK_ENV` 设置为 `production`
4. **备份**：定期备份 `data` 目录中的数据文件，以防数据丢失

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。
