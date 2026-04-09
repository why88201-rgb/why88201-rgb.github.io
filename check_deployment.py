"""
部署前检查脚本
检查项目是否准备好部署到Render等平台
"""
import os
import sys

def check_deployment_readiness():
    """检查部署准备情况"""
    print("=" * 60)
    print("部署前检查")
    print("=" * 60)
    
    checks = []
    
    # 检查必要文件
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.env.example',
        'README.md',
        'LICENSE',
        '.gitignore'
    ]
    
    print("\n[检查必要文件]")
    for file in required_files:
        exists = os.path.exists(file)
        status = "[OK]" if exists else "[X]"
        print(f"  {status} {file}")
        checks.append(exists)
    
    # 检查目录
    required_dirs = ['templates', 'data', 'uploads']
    print("\n[检查必要目录]")
    for dir_name in required_dirs:
        exists = os.path.isdir(dir_name)
        status = "[OK]" if exists else "[X]"
        print(f"  {status} {dir_name}/")
        checks.append(exists)
    
    # 检查数据文件
    data_files = [
        'data/uploaded_files.json',
        'data/registered_users.json',
        'data/registration_requests.json',
        'data/community_messages.json',
        'data/user_data.json',
        'data/form_fields.json'
    ]
    
    print("\n[检查数据文件]")
    for file in data_files:
        exists = os.path.exists(file)
        status = "[OK]" if exists else "[X]"
        print(f"  {status} {file}")
        checks.append(exists)
    
    # 检查环境变量
    print("\n[检查环境变量配置]")
    env_example_exists = os.path.exists('.env.example')
    env_exists = os.path.exists('.env')
    
    if env_example_exists:
        print("  [OK] .env.example 文件存在")
        checks.append(True)
    else:
        print("  [X] .env.example 文件不存在")
        checks.append(False)
    
    if env_exists:
        print("  [!] .env 文件存在（注意：此文件不应上传到GitHub）")
    else:
        print("  [OK] .env 文件不存在（将使用环境变量）")
    
    # 检查敏感文件是否在.gitignore中
    print("\n[检查.gitignore配置]")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        sensitive_items = ['.env', 'uploads/*', 'data/*']
        for item in sensitive_items:
            if item in gitignore_content:
                print(f"  [OK] {item} 已在.gitignore中")
                checks.append(True)
            else:
                print(f"  [X] {item} 未在.gitignore中")
                checks.append(False)
    else:
        print("  [X] .gitignore文件不存在")
        checks.append(False)
    
    # 总结
    print("\n" + "=" * 60)
    if all(checks):
        print("[SUCCESS] 所有检查通过！项目已准备好部署。")
        print("\n下一步操作：")
        print("1. 初始化Git仓库: git init")
        print("2. 添加所有文件: git add .")
        print("3. 提交更改: git commit -m 'Initial commit'")
        print("4. 添加远程仓库: git remote add origin <your-repo-url>")
        print("5. 推送到GitHub: git push -u origin main")
        print("6. 在Render上创建新的Web服务并连接到GitHub仓库")
        return 0
    else:
        print("[FAILED] 部分检查未通过，请修复后再部署。")
        return 1

if __name__ == '__main__':
    sys.exit(check_deployment_readiness())
