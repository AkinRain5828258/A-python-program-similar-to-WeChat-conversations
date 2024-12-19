import tkinter as tk
from tkinter import messagebox
import json
import uuid
import hashlib
import datetime
import os

# 用户信息文件路径
users_file = 'users.json'

# 加载用户数据
def load_users():
    """从文件中加载用户信息，若文件不存在则创建默认管理员账户。"""
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
            # 添加 is_banned 和 ban_end_time 字段，如果这些字段不存在
            for user in users.values():
                if 'is_banned' not in user:
                    user['is_banned'] = False
                if 'ban_end_time' not in user:
                    user['ban_end_time'] = None
            return users
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

# 保存用户数据
def save_users(users):
    """将用户信息保存到文件中。"""
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# 对密码进行哈希加密
def hash_password(password):
    """对密码进行哈希加密。"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 登录功能
def login(users, username, password):
    """登录功能，支持用户名登录。"""
    for user_uid, user_info in users.items():
        if user_info['username'] == username:
            if user_info['password'] == hash_password(password):
                return user_uid
            else:
                return None
    return None

# 显示用户菜单（查看留言，发送留言）
def show_user_menu(users, uid, root):
    """用户菜单，提供查看留言、发送留言和删除留言的选项。"""
    user_info = users[uid]
    menu = tk.Toplevel(root)
    menu.title("用户菜单")

    # 查看留言
    def view_messages():
        """查看留言"""
        messages = user_info['inbox']
        msg_str = "\n".join([f"来自 {msg['sender']} 的留言: {msg['message']}" for msg in messages]) if messages else "你还没有收到留言"
        messagebox.showinfo("留言", msg_str)

    # 发送留言
    def send_message():
        """发送留言"""
        receiver = receiver_entry.get()
        message = message_entry.get()
        if receiver and message:
            for user_uid, user in users.items():
                if user['username'] == receiver:
                    user['inbox'].append({
                        'sender': user_info['username'],
                        'message': message
                    })
                    save_users(users)
                    messagebox.showinfo("成功", "留言发送成功")
                    return
            messagebox.showerror("错误", "接收者用户名不存在")

    tk.Button(menu, text="查看留言", command=view_messages).pack(pady=10)
    tk.Label(menu, text="接收者用户名:").pack(pady=5)
    receiver_entry = tk.Entry(menu)
    receiver_entry.pack(pady=5)
    tk.Label(menu, text="留言内容:").pack(pady=5)
    message_entry = tk.Entry(menu)
    message_entry.pack(pady=5)
    tk.Button(menu, text="发送留言", command=send_message).pack(pady=10)
    tk.Button(menu, text="退出", command=menu.destroy).pack(pady=10)

# 显示管理员菜单（删除用户、提升用户为管理员等）
def show_admin_menu(users, uid, root):
    """管理员菜单，提供删除用户、提升用户为管理员、发送留言等选项。"""
    admin_info = users[uid]
    menu = tk.Toplevel(root)
    menu.title("管理员菜单")

    # 删除用户
    def delete_user():
        """删除用户"""
        user_uid = delete_user_entry.get()
        if user_uid in users:
            del users[user_uid]
            save_users(users)
            messagebox.showinfo("成功", "用户已删除")
        else:
            messagebox.showerror("错误", "用户不存在")

    # 提升为管理员
    def promote_to_admin():
        """提升用户为管理员"""
        user_uid = promote_user_entry.get()
        if user_uid in users:
            users[user_uid]['is_admin'] = True
            save_users(users)
            messagebox.showinfo("成功", "用户已提升为管理员")
        else:
            messagebox.showerror("错误", "用户不存在")

    tk.Label(menu, text="删除用户UID:").pack(pady=5)
    delete_user_entry = tk.Entry(menu)
    delete_user_entry.pack(pady=5)
    tk.Button(menu, text="删除用户", command=delete_user).pack(pady=10)

    tk.Label(menu, text="提升为管理员UID:").pack(pady=5)
    promote_user_entry = tk.Entry(menu)
    promote_user_entry.pack(pady=5)
    tk.Button(menu, text="提升为管理员", command=promote_to_admin).pack(pady=10)

    tk.Button(menu, text="退出", command=menu.destroy).pack(pady=10)

# 显示登录界面
def show_login_window(users, root):
    """显示登录界面"""
    def attempt_login():
        """尝试登录"""
        username = username_entry.get()
        password = password_entry.get()
        uid = login(users, username, password)
        if uid:
            messagebox.showinfo("成功", "登录成功")
            if users[uid]['is_admin']:
                show_admin_menu(users, uid, root)
            else:
                show_user_menu(users, uid, root)
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    login_window = tk.Toplevel(root)
    login_window.title("登录")

    tk.Label(login_window, text="用户名:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="密码:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="登录", command=attempt_login).pack(pady=10)

# 主程序入口
def main():
    """主程序入口"""
    root = tk.Tk()
    root.title("用户系统")

    users = load_users()

    # 打开登录界面
    def open_login_window():
        show_login_window(users, root)

    tk.Label(root, text="欢迎使用用户系统", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="登录", width=20, command=open_login_window).pack(pady=10)
    tk.Button(root, text="退出", width=20, command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
