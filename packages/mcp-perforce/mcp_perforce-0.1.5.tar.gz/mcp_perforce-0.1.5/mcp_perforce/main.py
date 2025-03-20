#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
import asyncio
from .perforce import mcp, init_default_config

async def main():
    """
    mcp-servers-perforce 命令行入口点
    """
    parser = argparse.ArgumentParser(description='mcp-servers-perforce - 用于与Perforce Swarm系统交互的工具')
    parser.add_argument('--p4config', type=str, default='p4config.json', help='Perforce配置文件路径')
    parser.add_argument('--version', action='store_true', help='显示版本信息')
    parser.add_argument('--serve', action='store_true', help='启动MCP服务器')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='服务器主机地址')
    parser.add_argument('--port', type=int, default=8000, help='服务器端口')
    
    args = parser.parse_args()
    
    # 显示版本信息
    if args.version:
        from . import __version__
        print(f"mcp-servers-perforce 版本: {__version__}")
        return
    
    # 检查配置文件
    if not os.path.exists(args.p4config):
        print(f"错误: 配置文件不存在: {args.p4config}")
        print("请创建配置文件，格式如下:")
        print("""
{
  "p4client": "your_client_name",
  "p4port": "your_p4_server:1666",
  "p4user": "your_username",
  "p4passwd": "your_password",
  "swarm_username": "your_swarm_username",
  "swarm_password": "your_swarm_password",
  "swarm_base_url": "https://your_swarm_server",
  "swarm_api_url": "https://your_swarm_server/api/v10"
}
        """)
        return
    
    # 初始化配置
    init_default_config()
    
    # 启动MCP服务器
    if args.serve:
        print(f"启动MCP服务器在 {args.host}:{args.port}...")
        await mcp.serve(host=args.host, port=args.port)
    else:
        print("mcp-servers-perforce 工具")
        print("使用 --serve 参数启动MCP服务器")
        print("使用 --help 查看帮助信息")

if __name__ == "__main__":
    asyncio.run(main()) 