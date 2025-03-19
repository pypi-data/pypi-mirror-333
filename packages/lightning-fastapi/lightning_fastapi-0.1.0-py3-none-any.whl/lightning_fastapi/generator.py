import os
import sys
import shutil
import subprocess
from pathlib import Path
import inquirer  # 交互式命令行


# ANSI颜色代码
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    YELLOW = "\033[33m"


def print_info(message, en_message=None):
    """打印信息消息
    
    Args:
        message: 中文消息 (不再使用)
        en_message: 英文消息，必须提供
    """
    # 提取消息中的emoji（如果有）
    emoji = ""
    
    # 检查是否以emoji开头
    first_word = message.split()[0] if message.split() else ""
    if any(ord(c) > 127 for c in first_word):  # 简单检查是否包含非ASCII字符
        parts = message.split(" ", 1)
        emoji = parts[0] + " "
    else:
        emoji = "ℹ️ "  # 默认使用信息emoji
    
    # 准备英文消息
    en_msg = en_message if en_message else "Information"
    
    # 打印格式: [INFO] emoji English
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {emoji}{en_msg}")


def print_success(message, en_message=None):
    """打印成功消息
    
    Args:
        message: 中文消息 (不再使用)
        en_message: 英文消息，必须提供
    """
    # 提取消息中的emoji（如果有）
    emoji = ""
    
    # 检查是否以emoji开头
    first_word = message.split()[0] if message.split() else ""
    if any(ord(c) > 127 for c in first_word):  # 简单检查是否包含非ASCII字符
        parts = message.split(" ", 1)
        emoji = parts[0] + " "
    else:
        emoji = "✅ "  # 默认使用成功emoji
    
    # 准备英文消息
    en_msg = en_message if en_message else "Success"
    
    # 打印格式: [SUCCESS] emoji English
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {emoji}{en_msg}")


def print_error(message, en_message=None):
    """打印错误消息
    
    Args:
        message: 中文消息 (不再使用)
        en_message: 英文消息，必须提供
    """
    # 提取消息中的emoji（如果有）
    emoji = ""
    
    # 检查是否以emoji开头
    first_word = message.split()[0] if message.split() else ""
    if any(ord(c) > 127 for c in first_word):  # 简单检查是否包含非ASCII字符
        parts = message.split(" ", 1)
        emoji = parts[0] + " "
    else:
        emoji = "❌ "  # 默认使用错误emoji
    
    # 准备英文消息
    en_msg = en_message if en_message else "Error"
    
    # 打印格式: [ERROR] emoji English
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {emoji}{en_msg}")


def check_git():
    """检查Git是否安装"""
    try:
        subprocess.run(
            ["git", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_docker():
    """检查Docker是否已安装"""
    try:
        subprocess.run(
            ["docker", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def create_project(project_name=None):
    """创建新的Lightning-FastAPI项目
    
    Args:
        project_name: 项目名称，如果未提供将交互式获取
    """
    # 打印欢迎信息
    print(f"""
{Colors.GREEN}⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️{Colors.RESET}
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│▗    ▝      ▐    ▗       ▝              ▗▄▄▖         ▗   ▗▖ ▗▄▄ ▗▄▄ │
│▐   ▗▄   ▄▄ ▐▗▖ ▗▟▄ ▗▗▖ ▗▄  ▗▗▖  ▄▄     ▐    ▄▖  ▄▖ ▗▟▄  ▐▌ ▐ ▝▌ ▐  │
│▐    ▐  ▐▘▜ ▐▘▐  ▐  ▐▘▐  ▐  ▐▘▐ ▐▘▜     ▐▄▄▖▝ ▐ ▐ ▝  ▐   ▌▐ ▐▄▟▘ ▐  │
│▐    ▐  ▐ ▐ ▐ ▐  ▐  ▐ ▐  ▐  ▐ ▐ ▐ ▐     ▐   ▗▀▜  ▀▚  ▐   ▙▟ ▐    ▐  │
│▐▄▄▖▗▟▄ ▝▙▜ ▐ ▐  ▝▄ ▐ ▐ ▗▟▄ ▐ ▐ ▝▙▜     ▐   ▝▄▜ ▝▄▞  ▝▄ ▐  ▌▐   ▗▟▄ │
│         ▖▐                      ▖▐                                 │
│         ▝▘                      ▝▘                                 │
└────────────────────────────────────────────────────────────────────┘
{Colors.GREEN}                                  By JY {Colors.RESET}

{Colors.GREEN}⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️{Colors.RESET}
""")

    # 检查Git
    if not check_git():
        print_error(
            "❌ 未检测到Git，请先安装Git: https://git-scm.com/downloads",
            "Git not detected, please install Git first: https://git-scm.com/downloads"
        )
        sys.exit(1)

    # 交互式询问项目名称
    if not project_name:
        questions = [
            inquirer.Text(
                "project_name", message="Please enter project name / 请输入项目名称", default="fastapi-starter"
            )
        ]
        answers = inquirer.prompt(questions)
        project_name = answers["project_name"]

    # 检查目录是否存在
    if os.path.exists(project_name):
        questions = [
            inquirer.Confirm(
                "overwrite",
                message=f"Directory {Colors.YELLOW}{project_name}{Colors.RESET} already exists, overwrite? / 目录 {Colors.YELLOW}{project_name}{Colors.RESET} 已存在，是否覆盖?",
                default=False,
            )
        ]
        answers = inquirer.prompt(questions)
        if not answers["overwrite"]:
            print_info(
                "ℹ️ 操作已取消",
                "Operation cancelled"
            )
            return

        # 删除现有目录
        shutil.rmtree(project_name)

    # 克隆仓库
    print_info(
        f"📦 正在克隆FastAPI Starter仓库到 {Colors.YELLOW}{project_name}{Colors.RESET}...",
        f"Cloning FastAPI Starter repository to {Colors.YELLOW}{project_name}{Colors.RESET}"
    )
    subprocess.run(
        [
            "git",
            "clone",
            "https://github.com/yiyuan9/lightning-fastapi.git",
            project_name,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    # 移除Git版本控制
    print_info(
        f"🧹 正在为 {Colors.YELLOW}{project_name}{Colors.RESET} 移除原始Git版本控制...",
        f"Removing original Git version control for {Colors.YELLOW}{project_name}{Colors.RESET}"
    )
    shutil.rmtree(os.path.join(project_name, ".git"))

    # 初始化新的Git仓库
    print_info(
        f"🔄 正在为 {Colors.YELLOW}{project_name}{Colors.RESET} 初始化新的Git仓库...",
        f"Initializing new Git repository for {Colors.YELLOW}{project_name}{Colors.RESET}"
    )
    subprocess.run(
        ["git", "init"],
        cwd=project_name,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    # 检查Docker安装
    docker_installed = check_docker()
    if docker_installed:
        print_success(
            "🐳 检测到Docker已安装，可以使用快速启动功能",
            "Docker is installed, quick start feature is available"
        )
    else:
        print_info(
            "🔍 未检测到Docker，请先安装Docker以使用快速启动功能: https://docs.docker.com/get-docker/",
            "Docker not detected, please install Docker to use quick start feature: https://docs.docker.com/get-docker/"
        )

    # 给脚本添加执行权限
    subprocess.run(
        ["chmod", "+x", os.path.join(project_name, "scripts/quickstart.sh")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    
    # 删除lightning_fastapi文件夹，保持项目结构干净
    lightning_fastapi_dir = os.path.join(project_name, 'lightning_fastapi')
    if os.path.exists(lightning_fastapi_dir):
        print_info(
            f"🧹 正在移除 {Colors.YELLOW}lightning_fastapi{Colors.RESET} 文件夹，确保项目结构干净整洁...",
            f"Removing {Colors.YELLOW}lightning_fastapi{Colors.RESET} folder to ensure clean project structure"
        )
        shutil.rmtree(lightning_fastapi_dir)

    # 打印成功消息
    print_success(
        f"🎉 {Colors.YELLOW}{project_name}{Colors.RESET} 项目已成功创建!",
        f"{Colors.YELLOW}{project_name}{Colors.RESET} project has been successfully created!"
    )

    # 自动使用 Docker 启动
    script_path = "scripts/quickstart.sh"
    print_info(
        f"🚀 正在使用 Docker 自动启动 {Colors.YELLOW}{project_name}{Colors.RESET} 项目...",
        f"Starting {Colors.YELLOW}{project_name}{Colors.RESET} project with Docker automatically"
    )
    try:
        subprocess.run([f"./{script_path}"], cwd=project_name, check=True)
        print_success(
            f"✅ {Colors.YELLOW}{project_name}{Colors.RESET} 项目启动成功！",
            f"{Colors.YELLOW}{project_name}{Colors.RESET} project started successfully!"
        )
        print(f"""
{Colors.GREEN}==================================${Colors.RESET}
🌍 Now you can access the API documentation / 现在您可以访问API文档:
{Colors.YELLOW}http://localhost:8000/docs{Colors.RESET}
{Colors.GREEN}==================================${Colors.RESET}
""")
    except subprocess.SubprocessError as e:
        print_error(
            f"❌ 启动失败: {str(e)}",
            f"Start failed: {str(e)}"
        )
        print(f"""
{Colors.GREEN}==================================${Colors.RESET}
You can manually start the project later / 您可以稍后手动启动项目:

1. Enter project directory / 进入项目目录:
   {Colors.YELLOW}cd {project_name}{Colors.RESET}

2. Start project / 启动项目:
   {Colors.YELLOW}./scripts/quickstart.sh{Colors.RESET}
{Colors.GREEN}==================================${Colors.RESET}
""")
        # 出错时询问是否重试
        questions = [
            inquirer.List(
                "retry_action",
                message="Do you want to retry starting the project? / 是否要重试启动项目？",
                choices=[
                    ("1. Retry start / 重试启动", "retry"),
                    ("2. Exit / 退出", "exit"),
                ],
                default="retry",
            )
        ]
        retry_answers = inquirer.prompt(questions)
        retry_choice = retry_answers["retry_action"]
        
        if retry_choice == "retry":
            # 进入项目目录
            os.chdir(project_name)
            print_info(
                f"📂 已进入项目目录: {Colors.YELLOW}{os.getcwd()}{Colors.RESET}",
                f"Entered project directory: {Colors.YELLOW}{os.getcwd()}{Colors.RESET}"
            )
            
            # 重试执行脚本
            print_info(
                f"🔄 正在重试执行 {script_path} 启动项目...",
                f"Retrying to start project with {script_path}"
            )
            try:
                subprocess.run([f"./{script_path}"], check=True)
                print_success(
                    "✅ 项目启动成功！",
                    "Project started successfully!"
                )
                print(f"""
{Colors.GREEN}==================================${Colors.RESET}
🌍 Now you can access the API documentation / 现在您可以访问API文档:
{Colors.YELLOW}http://localhost:8000/docs{Colors.RESET}
{Colors.GREEN}==================================${Colors.RESET}
""")
            except subprocess.SubprocessError:
                print_error(
                    "❌ 项目启动再次失败，请检查Docker环境后手动启动。",
                    "Project start failed again. Please check your Docker environment and start manually."
                )
                print(f"""
{Colors.GREEN}==================================${Colors.RESET}
Please ensure Docker and Docker Compose are installed and running properly / 请确保 Docker 和 Docker Compose 已安装并正常运行
Then manually execute / 然后手动执行:
{Colors.YELLOW}cd {project_name}{Colors.RESET}
{Colors.YELLOW}./scripts/quickstart.sh{Colors.RESET}
{Colors.GREEN}==================================${Colors.RESET}
""")
