import os
import json

# 用户信息文件路径
users_file = 'users.json'

admin_username = 'admin'
admin_password = '570848069'

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

def login():
    # 获取用户输入的用户名和密码
    username = input("请输入用户名：")
    password = input("请输入密码：")

    # 验证用户名和密码
    if username == admin_username and password == admin_password:
        print("管理员登录成功！")
        show_admin_menu()
        return None
    elif username in users and users[username]['password'] == password:
        print("用户登录成功！")
        return username
    else:
        print("登录失败，用户名或密码错误！")
        return None

def register():
    # 用户注册
    username = input("请输入新的用户名：")
    if username in users:
        print("用户名已存在！")
        return None
    password = input("请输入新的密码：")
    users[username] = {'password': password, 'messages': []}
    save_users(users)
    print("注册成功！")
    return username

def change_password(username):
    # 修改密码
    old_password = input("请输入旧密码：")
    if users[username]['password'] == old_password:
        new_password = input("请输入新密码：")
        users[username]['password'] = new_password
        save_users(users)
        print("密码修改成功！")
    else:
        print("旧密码错误！")

def send_message(sender, receiver):
    # 发送留言
    message = input("请输入你的留言：")
    if receiver in users:
        users[receiver]['messages'].append({'sender': sender, 'message': message})
        save_users(users)
        print("留言成功！")
    else:
        print("接收留言的用户不存在！")

def load_messages(username):
    # 读取用户留言
    return users[username]['messages']

def show_admin_menu():
    while True:
        print("\n请选择操作：")
        print("1. 删除用户")
        print("2. 返回主菜单")
        choice = input("请输入选项（1/2）：")

        if choice == "1":
            delete_user()
        elif choice == "2":
            print("返回主菜单。")
            break
        else:
            print("无效的选项，请重新输入！")

def delete_user():
    username = input("请输入要删除的用户名：")
    if username in users:
        del users[username]
        save_users(users)
        print("用户已删除！")
    else:
        print("用户不存在！")

def show_menu():
    while True:
        print("\n请选择操作：")
        print("1. 登录")
        print("2. 注册")
        print("3. 修改密码")
        print("4. 发送留言")
        print("5. 退出")
        choice = input("请输入选项（1/2/3/4/5）：")

        if choice == "1":
            username = login()
            if username:
                show_user_menu(username)
        elif choice == "2":
            username = register()
            if username:
                show_user_menu(username)
        elif choice == "3":
            username = input("请输入用户名：")
            if username in users:
                change_password(username)
            else:
                print("用户名不存在！")
        elif choice == "4":
            sender = input("请输入你的用户名：")
            if sender in users:
                receiver = input("请输入接收留言的用户名：")
                send_message(sender, receiver)
            else:
                print("你的用户名不存在！")
        elif choice == "5":
            print("退出系统。")
            break
        else:
            print("无效的选项，请重新输入！")

def show_user_menu(username):
    while True:
        print("\n请选择操作：")
        print("1. 查看留言")
        print("2. 返回主菜单")
        choice = input("请输入选项（1/2）：")

        if choice == "1":
            messages = load_messages(username)
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

# 加载用户信息
users = load_users()

def main():
    show_menu()

if __name__ == "__main__":
    main()
