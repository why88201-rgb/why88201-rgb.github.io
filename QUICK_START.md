# 快速使用指南

## 可用脚本

### Windows用户

#### 1. 启动网站
双击运行 `start.bat`
- 自动检查Python环境
- 自动安装依赖
- 自动初始化数据文件
- 启动网站服务器

#### 2. 部署到GitHub
双击运行 `deploy_github.bat`
- 运行部署前检查
- 初始化Git仓库
- 添加和提交文件
- 提供后续部署指导

### 命令行用户

#### 启动网站
```bash
python app.py
```

#### 初始化数据文件
```bash
python init_data.py
```

#### 部署前检查
```bash
python check_deployment.py
```

#### 部署到GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

## 访问地址

启动网站后，可通过以下地址访问：

- **本地访问**: http://127.0.0.1:5000
- **局域网访问**: http://192.168.3.106:5000

## 默认账户

### 管理员账户
- 用户名: `admin`
- 密码: `admin123`

## 功能说明

### 用户功能
- 注册账户（需要管理员审核）
- 登录系统
- 浏览已上传文件
- 信息收集填写
- 社区留言

### 管理员功能
- 文件上传（最大5GB）
- 删除文件
- 审核注册申请
- 查看用户信息收集
- 编辑信息收集表单
- 导出用户数据为Excel

## 支持的文件类型

- **图片**: jpg, jpeg, png, gif
- **音频**: mp3, wav, flac, ogg, aac
- **视频**: mp4

## 常见问题

### Q: 启动时提示端口被占用
A: 修改 `app.py` 最后一行的端口号，例如改为 `port=5001`

### Q: 上传文件失败
A: 检查 `uploads` 目录是否存在且有写入权限

### Q: 数据丢失
A: 检查 `data` 目录中的JSON文件是否存在

### Q: 无法登录
A: 
1. 检查用户名和密码是否正确
2. 检查 `data/registered_users.json` 文件
3. 管理员账户默认: admin/admin123

## 技术支持

如有问题，请查看：
- `README.md` - 完整项目说明
- `DEPLOYMENT_REPORT.md` - 部署报告
- `.env.example` - 环境变量配置示例
