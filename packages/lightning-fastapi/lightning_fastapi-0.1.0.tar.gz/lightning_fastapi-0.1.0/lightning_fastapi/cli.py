#!/usr/bin/env python3
import argparse
import os
import sys
from .generator import create_project


def main():
    """FastAPI Starter CLI entry point / 入口点"""
    parser = argparse.ArgumentParser(description="Create FastAPI project scaffold / 创建FastAPI项目脚手架")
    parser.add_argument("project_name", nargs="?", default=None, help="Project name / 项目名称")

    args = parser.parse_args()

    try:
        create_project(args.project_name)
    except KeyboardInterrupt:
        print("\nOperation cancelled / 操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"Error / 错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
