"""
CetherOS v0.1 Simulation (Windows适配修复版)
激活码：CETHER‑DEV‑PERMANENT‑2026
"""
import os
import sys
import socket
import subprocess
import psutil
import cpuinfo
from pynput import keyboard


class UEFISimulator:
    def __init__(self):
        self.version = "UEFI 2.10"

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def boot_animation(self):
        self.clear_screen()
        print(f"===== {self.version} Firmware Initializing =====")
        print("[OK] Memory Initialized")
        print("[OK] Storage Controller Loaded")
        print("[INFO] Detect Virtual Machine, skip extra hardware check\n")


def user_activation_flow(user_type: int):
    dev_key = "CETHER‑DEV‑PERMANENT‑2026"
    if user_type == 1:
        print("\n----- Developer Mode Activation -----")
        input_key = input("请输入开发者激活码：")
        if input_key.strip() != dev_key:
            print("[ERROR] 激活码无效，程序终止")
            sys.exit(1)
        print("[SUCCESS] 开发者权限已解锁")
        return "developer"
    elif user_type == 2:
        print("\n----- Guest User Mode -----")
        print("[INFO] 访客模式：高级模块已禁用")
        return "user"
    elif user_type == 3:
        print("\n----- Enterprise Mode -----")
        print("[WARN] 企业授权暂未实现")
        sys.exit(1)
    else:
        print("[ERROR] 无效选项")
        sys.exit(1)


def run_developer_shell():
    """开发者交互控制台"""
    print("\n======== CetherOS Developer Shell ========")
    print("命令：help | shutdown | server | lib")
    while True:
        cmd = input("CetherOS~# ").strip().lower()
        if cmd == "help":
            print("help      显示帮助")
            print("shutdown  关闭仿真系统")
            print("server    启动5900简易socket服务")
            print("lib       查看系统加载库")
        elif cmd == "shutdown":
            print("系统正在关闭...")
            break
        elif cmd == "server":
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("192.168.0.1", 5900))
                s.listen(1)
                print("[SERVER] 监听 192.168.0.1:5900")
                s.close()
            except Exception as e:
                print(f"[SERVER ERROR] {e}")
        elif cmd == "lib":
            print(f"psutil: ok | cpuinfo: ok | socket: ok | subprocess: ok")
        else:
            print(f"未知命令: {cmd}")


def run_guest_shell():
    """访客模式，禁用高危模块"""
    print("\n======== CetherOS Guest Shell ========")
    print("仅基础功能可用，socket/subprocess已隔离")
    while True:
        c = input("CetherOS$ ").strip().lower()
        if c == "shutdown":
            print("退出访客会话")
            break
        elif c == "help":
            print("help / shutdown")
        else:
            print("指令不支持")


def install_wizard():
    uefi = UEFISimulator()
    uefi.boot_animation()

    print(r"""
   _____          _    ____  _____
  / ____|        | |  / __ \|  __ \
 | |     ___ _ __| |_| |  | | |__) |
 | |    / _ \ '__| __| |  | |  ___/
 | |___|  __/ |  | |_| |__| | |
  \_____\___|_|   \__|\____/|_|
        CetherOS v0.1 SIMULATOR
    """)
    print("请选择用户类型：")
    print("1 = Developer(开发者)")
    print("2 = User(访客)")
    print("3 = Enterprise(企业)")

    try:
        sel = int(input("输入序号 [1/2/3]："))
    except ValueError:
        print("输入错误，退出")
        return

    selected_user = user_activation_flow(sel)

    if selected_user == "developer":
        run_developer_shell()
    elif selected_user == "user":
        run_guest_shell()


if __name__ == "__main__":
    install_wizard()
