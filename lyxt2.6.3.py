import os
import json
import uuid
import datetime
import hashlib

# 用户信息文件路径
users_file = 'users.json'

def hash_password(password):
    """对密码进行哈希加密"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_users():
    """从文件中加载用户信息，若文件不存在则创建默认管理员账户。"""
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                users = json.load(f)
                # 添加 is_banned 和 ban_end_time 字段，如果这些字段不存在
                for user in users.values():
                    if 'is_banned' not in user:
                        user['is_banned'] = False
                    if 'ban_end_time' not in user:
                        user['ban_end_time'] = None
                return users
        except (FileNotFoundError, json.JSONDecodeError):
            print("用户文件读取失败，创建新的用户数据文件...")
            return {}
    else:
        admin_info = {
            'username': 'admin',
            'password': hash_password('123456'),
            'is_admin': True,
            'messages': [],
            'inbox': [],
            'is_banned': False,
            'ban_end_time': None
        }
        users = {str(uuid.uuid4()): admin_info}
        save_users(users)
        return users

def save_users(users):
    """将用户信息保存到文件中。"""
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

def register(users):
    """用户注册，检查用户名是否已存在。"""
    while True:
        username = input("请输入新的用户名：")
        if any(user['username'] == username for user in users.values()):
            print("用户名已存在！")
            continue
        password = input("请输入新的密码：")
        uid = str(uuid.uuid4())
        users[uid] = {
            'username': username,
            'password': hash_password(password),
            'is_admin': False,
            'messages': [],
            'inbox': [],
            'is_banned': False,
            'ban_end_time': None
        }
        save_users(users)
        print("注册成功！你的UID是：", uid)
        return uid

def login(users):
    """登录，支持通过UID或用户名登录。"""
    while True:
        login_type = input("请选择登录方式（1. UID；2. 用户名）：")
        if login_type == '1':
            uid = input("请输入UID：")
            if uid in users:
                if users[uid]['is_banned']:
                    if users[uid]['ban_end_time'] is None or users[uid]['ban_end_time'] <= datetime.datetime.now():
                        users[uid]['is_banned'] = False
                        users[uid]['ban_end_time'] = None
                        save_users(users)
                        print("封号已结束，用户已解封！")
                    else:
                        print("登录失败，用户被封号！")
                        return None
                password = input("请输入密码：")
                if users[uid]['password'] == hash_password(password):
                    return uid
                else:
                    print("登录失败，UID或密码错误！")
                    return None
            else:
                print("用户不存在！")
                return None
        elif login_type == '2':
            username = input("请输入用户名：")
            password = input("请输入密码：")
            for user_uid, user_info in users.items():
                if user_info['username'] == username:
                    if user_info['is_banned']:
                        if user_info['ban_end_time'] is None or user_info['ban_end_time'] <= datetime.datetime.now():
                            users[user_uid]['is_banned'] = False
                            users[user_uid]['ban_end_time'] = None
                            save_users(users)
                            print("封号已结束，用户已解封！")
                        else:
                            print("登录失败，用户被封号！")
                            return None
                    if user_info['password'] == hash_password(password):
                        return user_uid
            print("登录失败，用户名或密码错误！")
            return None
        else:
            print("无效的选项，请重新输入！")

def change_password(users, uid):
    """修改密码，验证旧密码是否正确。"""
    while True:
        old_password = input("请输入旧密码：")
        if users[uid]['password'] == hash_password(old_password):
            new_password = input("请输入新密码：")
            users[uid]['password'] = hash_password(new_password)
            save_users(users)
            print("密码修改成功！")
            return
        else:
            print("旧密码错误！")

def delete_user(users):
    """删除用户，确认UID存在。"""
    uid = input("请输入要删除的用户的UID：")
    if uid in users:
        del users[uid]
        save_users(users)
        print("用户已删除！")
    else:
        print("用户不存在！")

def promote_to_admin(users):
    """提升用户为管理员，确认UID存在。"""
    uid = input("请输入要提升为管理员的用户的UID：")
    if uid in users:
        if users[uid]['is_admin']:
            print("该用户已经是管理员！")
        else:
            users[uid]['is_admin'] = True
            save_users(users)
            print("用户已成功提升为管理员！")
    else:
        print("用户不存在！")

def send_message(users, sender_uid):
    """发送留言，确认接收者UID存在。"""
    receiver_uid = input("请输入接收者的UID：")
    if receiver_uid in users:
        message = input("请输入留言：")
        users[receiver_uid]['inbox'].append({
            'sender': users[sender_uid]['username'],
            'message': message
        })
        save_users(users)
        print("留言发送成功！")
    else:
        print("接收者不存在！")

def delete_message(users, uid):
    """删除留言，确认留言存在。"""
    if len(users[uid]['inbox']) == 0:
        print("没有留言可以删除！")
        return
    try:
        message_index = int(input("请输入要删除的留言的序号：")) - 1
        if 0 <= message_index < len(users[uid]['inbox']):
            del users[uid]['inbox'][message_index]
            save_users(users)
            print("留言删除成功！")
        else:
            print("留言序号无效！")
    except ValueError:
        print("请输入有效的数字序号！")

def show_messages(users, uid):
    """查看留言，确认留言存在。"""
    messages = users[uid]['inbox']
    if messages:
        print(f"这是你的留言：")
        for i, message in enumerate(messages, 1):
            print(f"{i}. 来自 {message['sender']} 的留言：{message['message']}")
    else:
        print("你还没有收到任何留言。")

def ban_user(users):
    """封号用户，确认UID存在。"""
    uid = input("请输入要封号的用户的UID：")
    if uid in users:
        while True:
            try:
                ban_end_time = input("请输入封号结束时间（格式：YYYY-MM-DD HH:MM:SS）：")
                ban_end_time = datetime.datetime.strptime(ban_end_time, '%Y-%m-%d %H:%M:%S')
                users[uid]['is_banned'] = True
                users[uid]['ban_end_time'] = ban_end_time
                save_users(users)
                print("用户已封号！")
                break
            except ValueError:
                print("无效的时间格式，请重新输入！")
    else:
        print("用户不存在！")

def unban_user(users):
    """解封用户，确认UID存在。"""
    uid = input("请输入要解封的用户的UID：")
    if uid in users:
        if users[uid]['is_banned']:
            users[uid]['is_banned'] = False
            users[uid]['ban_end_time'] = None
            save_users(users)
            print("用户已解封！")
        else:
            print("用户未被封号！")
    else:
        print("用户不存在！")

def show_admin_menu(users, uid):
    """管理员菜单，提供删除用户、提升用户为管理员、发送留言、查看所有用户留言、预创建账户、封号用户和解封用户的选项。"""
    while True:
        print("\n请选择操作：")
        print("1. 删除用户")
        print("2. 提升用户为管理员")
        print("3. 发送留言")
        print("4. 查看所有用户留言")
        print("5. 查看我的留言")
        print("6. 预创建账户")
        print("7. 封号用户")
        print("8. 解封用户")
        print("9. 返回主菜单")
        choice = input("请输入选项（1/2/3/4/5/6/7/8/9）：")
        if choice == "1":
            delete_user(users)
        elif choice == "2":
            promote_to_admin(users)
        elif choice == "3":
            send_message(users, uid)
        elif choice == "4":
            for user_uid, user_info in users.items():
                                print(f"用户 {user_info['username']} 的留言：")
                for message in user_info['inbox']:
                    print(f"  - 来自 {message['sender']} 的留言：{message['message']}")
        elif choice == "5":
            show_messages(users, uid)
        elif choice == "6":
            # 创建新账户
            register(users)
        elif choice == "7":
            ban_user(users)
        elif choice == "8":
            unban_user(users)
        elif choice == "9":
            break
        else:
            print("无效的选项，请重新输入！")

def main():
    """主程序入口"""
    users = load_users()

    while True:
        print("\n欢迎来到系统，请选择操作：")
        print("1. 登录")
        print("2. 注册")
        print("3. 退出")
        choice = input("请输入选项（1/2/3）：")

        if choice == '1':
            uid = login(users)
            if uid:
                print(f"欢迎 {users[uid]['username']}！")
                if users[uid]['is_admin']:
                    show_admin_menu(users, uid)
                else:
                    print("你是普通用户，无法访问管理员功能。")
            else:
                print("登录失败！")
        elif choice == '2':
            uid = register(users)
            print(f"注册成功，UID：{uid}")
        elif choice == '3':
            print("退出系统，感谢使用！")
            break
        else:
            print("无效的选项，请重新选择！")

if __name__ == "__main__":
    main()
