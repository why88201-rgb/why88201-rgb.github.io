from flask import Flask, request, render_template, send_file, redirect, url_for, session, send_from_directory
import os
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB限制
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # 用于会话管理

# 数据文件路径
DATA_DIR = 'data'
UPLOADED_FILES_FILE = os.path.join(DATA_DIR, 'uploaded_files.json')
REGISTERED_USERS_FILE = os.path.join(DATA_DIR, 'registered_users.json')
REGISTRATION_REQUESTS_FILE = os.path.join(DATA_DIR, 'registration_requests.json')
COMMUNITY_MESSAGES_FILE = os.path.join(DATA_DIR, 'community_messages.json')
USER_DATA_FILE = os.path.join(DATA_DIR, 'user_data.json')
FORM_FIELDS_FILE = os.path.join(DATA_DIR, 'form_fields.json')

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'jpg', 'jpeg', 'png', 'gif', 'wav', 'flac', 'ogg', 'aac'}

# 管理员账户
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# 存储用户数据
user_data = []

# 存储上传的文件信息
uploaded_files = []

# 存储注册用户信息
registered_users = {
    'admin': ADMIN_PASSWORD  # 管理员账户
}

# 存储注册申请
registration_requests = []

# 存储社区留言
community_messages = []

# 加载数据
def load_data():
    global uploaded_files, registered_users, registration_requests, community_messages, user_data, form_fields
    
    # 加载上传的文件信息
    if os.path.exists(UPLOADED_FILES_FILE):
        try:
            with open(UPLOADED_FILES_FILE, 'r', encoding='utf-8') as f:
                uploaded_files = json.load(f)
        except:
            uploaded_files = []
    
    # 加载注册用户信息
    if os.path.exists(REGISTERED_USERS_FILE):
        try:
            with open(REGISTERED_USERS_FILE, 'r', encoding='utf-8') as f:
                registered_users = json.load(f)
        except:
            registered_users = {'admin': ADMIN_PASSWORD}
    
    # 加载注册申请
    if os.path.exists(REGISTRATION_REQUESTS_FILE):
        try:
            with open(REGISTRATION_REQUESTS_FILE, 'r', encoding='utf-8') as f:
                registration_requests = json.load(f)
        except:
            registration_requests = []
    
    # 加载社区留言
    if os.path.exists(COMMUNITY_MESSAGES_FILE):
        try:
            with open(COMMUNITY_MESSAGES_FILE, 'r', encoding='utf-8') as f:
                community_messages = json.load(f)
        except:
            community_messages = []
    
    # 加载用户数据
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        except:
            user_data = []
    
    # 加载表单字段信息
    if os.path.exists(FORM_FIELDS_FILE):
        try:
            with open(FORM_FIELDS_FILE, 'r', encoding='utf-8') as f:
                form_fields = json.load(f)
        except:
            form_fields = [
                {'name': 'name', 'label': '姓名', 'type': 'text', 'required': True},
                {'name': 'email', 'label': '邮箱', 'type': 'email', 'required': True}
            ]

# 保存数据
def save_data():
    # 保存上传的文件信息
    with open(UPLOADED_FILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(uploaded_files, f, ensure_ascii=False, indent=2)
    
    # 保存注册用户信息
    with open(REGISTERED_USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(registered_users, f, ensure_ascii=False, indent=2)
    
    # 保存注册申请
    with open(REGISTRATION_REQUESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(registration_requests, f, ensure_ascii=False, indent=2)
    
    # 保存社区留言
    with open(COMMUNITY_MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(community_messages, f, ensure_ascii=False, indent=2)
    
    # 保存用户数据
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    # 保存表单字段信息
    with open(FORM_FIELDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(form_fields, f, ensure_ascii=False, indent=2)

# 初始加载数据
load_data()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', is_admin=session.get('is_admin'), uploaded_files=uploaded_files, session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if action == 'login':
            # 登录逻辑
            if username in registered_users and registered_users[username] == password:
                session['is_admin'] = (username == ADMIN_USERNAME)
                session['username'] = username
                return redirect(url_for('index'))
            return render_template('login.html', error='用户名或密码错误')
        elif action == 'register':
            # 注册逻辑
            if username in registered_users:
                return render_template('login.html', error='用户名已存在')
            
            # 获取额外的注册信息
            qq = request.form.get('qq')
            bilibili_id = request.form.get('bilibili_id')
            
            # 处理B站粉丝牌文件上传
            bilibili_fans = ''
            if 'bilibili_fans' in request.files:
                file = request.files['bilibili_fans']
                if file and file.filename != '':
                    # 保存文件
                    filename = f"bilibili_fans_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    bilibili_fans = filename
            
            # 创建注册申请
            registration_request = {
                'username': username,
                'password': password,
                'qq': qq,
                'bilibili_id': bilibili_id,
                'bilibili_fans': bilibili_fans,
                'status': 'pending',  # pending, approved, rejected
                'request_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 添加到注册申请列表
            registration_requests.append(registration_request)
            
            # 保存数据
            save_data()
            
            # 显示注册申请成功消息
            return render_template('login.html', error='注册申请已提交，请等待管理员审核')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # 保存文件
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 更新上传文件列表
        file_info = {
            'filename': filename,
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        uploaded_files.append(file_info)
        
        # 保存数据
        save_data()
        
        return render_template('success.html', filename=filename)
    
    return redirect(request.url)

def generate_excel():
    if user_data:
        df = pd.DataFrame(user_data)
        excel_path = 'user_data.xlsx'
        df.to_excel(excel_path, index=False)
        return excel_path
    return None

# 存储表单字段信息
form_fields = [
    {'name': 'name', 'label': '姓名', 'type': 'text', 'required': True},
    {'name': 'email', 'label': '邮箱', 'type': 'email', 'required': True}
]

@app.route('/info_collect', methods=['GET', 'POST'])
def info_collect():
    # 检查用户是否登录
    if not session.get('username'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 收集用户信息
        user_info = {
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        for field in form_fields:
            user_info[field['name']] = request.form.get(field['name'], '')
        
        user_data.append(user_info)
        
        # 生成Excel文件
        generate_excel()
        
        # 保存数据
        save_data()
        
        return render_template('success.html', filename='信息收集')
    
    return render_template('info_collect.html', form_fields=form_fields)

@app.route('/edit_info_form', methods=['GET', 'POST'])
def edit_info_form():
    # 检查是否为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    global form_fields
    
    if request.method == 'POST':
        # 更新表单字段
        form_fields = []
        field_count = int(request.form.get('field_count', 0))
        for i in range(field_count):
            name = request.form.get(f'field_name_{i}')
            label = request.form.get(f'field_label_{i}')
            field_type = request.form.get(f'field_type_{i}')
            required = request.form.get(f'field_required_{i}') == 'on'
            if name and label:
                form_fields.append({'name': name, 'label': label, 'type': field_type, 'required': required})
        
        # 保存数据
        save_data()
        
        return redirect(url_for('info_collect'))
    
    return render_template('edit_info_form.html', form_fields=form_fields)

@app.route('/view_file/<int:file_id>')
def view_file(file_id):
    # 检查是否登录
    if not session.get('username'):
        return redirect(url_for('login'))
    
    if file_id < len(uploaded_files):
        file_info = uploaded_files[file_id]
        filename = file_info['filename']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(file_path):
            # 根据文件类型返回不同的内容
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return send_file(file_path, mimetype='image/' + filename.rsplit('.', 1)[1].lower())
            elif filename.endswith(('.mp3', '.wav', '.flac', '.ogg', '.aac')):
                # 确定音频文件的MIME类型
                ext = filename.rsplit('.', 1)[1].lower()
                mime_type = 'audio/mpeg' if ext == 'mp3' else \
                           'audio/wav' if ext == 'wav' else \
                           'audio/flac' if ext == 'flac' else \
                           'audio/ogg' if ext == 'ogg' else \
                           'audio/aac'
                return f"<audio controls><source src='/uploads/{filename}' type='{mime_type}'>Your browser does not support the audio element.  </audio>"
            elif filename.endswith('.mp4'):
                return f"<video controls><source src='/uploads/{filename}' type='video/mp4'>Your browser does not support the video element.</video>"
            else:
                return send_file(file_path, as_attachment=True)
    return 'File not found'

@app.route('/download_excel')
def download_excel():
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    excel_path = generate_excel()
    if excel_path and os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True)
    return 'No data available'

@app.route('/view_user_data')
def view_user_data():
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    return render_template('view_user_data.html', user_data=user_data)

@app.route('/review_registration')
def review_registration():
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    return render_template('review_registration.html', registration_requests=registration_requests)

@app.route('/approve_registration/<int:request_id>')
def approve_registration(request_id):
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request_id < len(registration_requests):
        request = registration_requests[request_id]
        request['status'] = 'approved'
        # 将用户添加到已注册用户列表
        registered_users[request['username']] = request['password']
        
        # 保存数据
        save_data()
    
    return redirect(url_for('review_registration'))

@app.route('/reject_registration/<int:request_id>')
def reject_registration(request_id):
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request_id < len(registration_requests):
        registration_requests[request_id]['status'] = 'rejected'
        
        # 保存数据
        save_data()
    
    return redirect(url_for('review_registration'))

# 静态文件服务

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/community', methods=['GET', 'POST'])
def community():
    # 检查用户是否登录
    if not session.get('username'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 提交留言
        message = request.form.get('message')
        if message:
            message_info = {
                'username': session.get('username'),
                'message': message,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            community_messages.append(message_info)
            
            # 保存数据
            save_data()
            
            return redirect(url_for('community'))
    
    return render_template('community.html', messages=community_messages, session=session)

@app.route('/delete_file/<int:file_id>')
def delete_file(file_id):
    # 检查是否登录为管理员
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if file_id < len(uploaded_files):
        # 获取文件信息
        file_info = uploaded_files[file_id]
        filename = file_info['filename']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 删除实际文件
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 从上传文件列表中删除
        uploaded_files.pop(file_id)
        
        # 保存数据
        save_data()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
