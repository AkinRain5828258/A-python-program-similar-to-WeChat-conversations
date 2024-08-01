import os
import json
import uuid

# 用户信息文件路径
users_file = 'users.json'

def load_users():
    # 从文件中加载用户信息
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    # 将用户信息保存到文件中
    with open(users_file, 'w') as f:
        json.dump(users, f)

def register():
    # 用户注册
    username = input("请输入新的用户名：")
    if username in [user['username'] for user in users.values()]:
        print("用户名已存在！")
        return None
    password = input("请输入新的密码：")
    uid = str(uuid.uuid4())
    is_admin = input("是否为管理员账户？(y/n)").lower() == 'y'
    users[uid] = {'username': username, 'password': password, 'is_admin': is_admin, 'messages': []}
    save_users(users)
    print("注册成功！你的UID是：", uid)
    return uid

def login():
    # 获取用户输入的登录方式和凭证
    login_type = input("请选择登录方式（1. UID；2. 用户名）：")
    if login_type == '1':
        uid = input("请输入UID：")
        password = input("请输入密码：")
        # 验证UID和密码
        if uid in users and users[uid]['password'] == password:
            return uid
        else:
            print("登录失败，UID或密码错误！")
            return None
    elif login_type == '2':
        username = input("请输入用户名：")
        password = input("请输入密码：")
        # 验证用户名和密码
        uid = None
        for user_uid, user_info in users.items():
            if user_info['username'] == username and user_info['password'] == password:
                uid = user_uid
                break
        if uid:
            return uid
        else:
            print("登录失败，用户名或密码错误！")
            return None
    else:
        print("无效的选项，请重新输入！")
        return None

def change_password(uid):
    # 修改密码
    old_password = input("请输入旧密码：")
    if users[uid]['password'] == old_password:
        new_password = input("请输入新密码：")
        users[uid]['password'] = new_password
        save_users(users)
        print("密码修改成功！")
    else:
        print("旧密码错误！")

def delete_user():
    uid = input("请输入要删除的用户的UID：")
    if uid in users:
        del users[uid]
        save_users(users)
        print("用户已删除！")
    else:
        print("用户不存在！")

def modify_user():
    uid = input("请输入要修改的用户的UID：")
    if uid in users:
        new_password = input("请输入新的密码：")
        users[uid]['password'] = new_password
        save_users(users)
        print("用户信息已修改！")
    else:
        print("用户不存在！")

def send_message(sender_uid, receiver_uid):
    # 发送留言
    message = input("请输入你的留言：")
    if receiver_uid in users:
        users[receiver_uid]['messages'].append({'sender': users[sender_uid]['username'], 'message': message})
        save_users(users)
        print("留言成功！")
    else:
        print("接收留言的用户不存在！")

def load_messages(uid):
    # 读取用户留言
    return users[uid]['messages']

def show_admin_menu(uid):
    while True:
        print("\n请选择操作：")
        print("1. 删除用户")
        print("2. 修改用户信息")
        print("3. 返回主菜单")
        choice = input("请输入选项（1/2/3）：")

        if choice == "1":
            delete_user()
        elif choice == "2":
            modify_user()
        elif choice == "3":
            print("返回主菜单。")
            break
        else:
            print("无效的选项，请重新输入！")

def show_user_menu(uid):
    while True:
        print("\n请选择操作：")
        print("1. 查看留言")
        print("2. 返回主菜单")
        choice = input("请输入选项（1/2）：")

        if choice == "1":
            messages = load_messages(uid)
            if messages:
                print(f"这是你的留言：")
                for message in messages:
                    print(f"来自 {message['sender']} 的留言：{message['message']}")
            else:
                print("你还没有收到任何留言。")
        elif choice == "2":
            print("返回主菜单。")
            break
        else:
            print("无效的选项，请重新输入！")

def show_menu():
    while True:
        print("\n请选择操作：")
        print("1. 登录")
        print("2. 注册")
        print("3. 修改密码")
        print("4. 退出")
        choice = input("请输入选项（1/2/3/4）：")

        if choice == "1":
            uid = login()
            if uid:
                if users[uid]['is_admin']:
                    show_admin_menu(uid)
                else:
                    show_user_menu(uid)
        elif choice == "2":
            uid = register()
            if uid:
                if users[uid]['is_admin']:
                    show_admin_menu(uid)
                else:
                    show_user_menu(uid)
        elif choice == "3":
            uid = input("请输入UID：")
            if uid in users:
                change_password(uid)
            else:
                print("UID不存在！")
        elif choice == "4":
            print("退出系统。")
            break
        else:
            print("无效的选项，请重新输入！")

# 加载用户信息
users = load_users()

def main():
    show_menu()

if __name__ == "__main__":
    main()
