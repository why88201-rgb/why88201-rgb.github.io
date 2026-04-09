"""
初始化数据文件脚本
在首次部署或重置应用时运行此脚本
"""
import json
import os

DATA_DIR = 'data'

def init_data_files():
    """初始化所有数据文件"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    data_files = {
        'uploaded_files.json': [],
        'registered_users.json': {'admin': 'admin123'},
        'registration_requests.json': [],
        'community_messages.json': [],
        'user_data.json': [],
        'form_fields.json': [
            {'name': 'name', 'label': '姓名', 'type': 'text', 'required': True},
            {'name': 'email', 'label': '邮箱', 'type': 'email', 'required': True}
        ]
    }
    
    for filename, initial_data in data_files.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            print(f"✓ 已创建: {filepath}")
        else:
            print(f"⊗ 已存在: {filepath}")
    
    print("\n数据文件初始化完成！")

if __name__ == '__main__':
    init_data_files()
