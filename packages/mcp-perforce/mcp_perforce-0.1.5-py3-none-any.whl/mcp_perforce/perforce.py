from typing import Any, Dict, List, Optional
import subprocess
import json
import re
import requests
import base64
import os
from mcp.server.fastmcp import FastMCP
import datetime
from bs4 import BeautifulSoup
import time

# Initialize FastMCP server
mcp = FastMCP("p4")

# Constants
P4_CMD = "p4"  # Perforce command line executable
P4_DEFAULT_CLIENT = None  # 默认的Perforce客户端
P4_DEFAULT_PORT = None    # 默认的Perforce服务器地址
P4_DEFAULT_USER = None    # 默认的Perforce用户名
P4_DEFAULT_PASSWD = None  # 默认的Perforce密码

# Swarm相关常量
SWARM_BASE_URL = None
SWARM_API_URL = None
SWARM_USERNAME = None
SWARM_PASSWORD = None

# 从配置文件读取P4配置
def read_p4_config_file(config_file_path):
    try:
        if not os.path.exists(config_file_path):
            print(f"配置文件不存在: {config_file_path}")
            return None
        
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return {
            'p4client': config.get('p4client'),
            'p4port': config.get('p4port'),
            'p4user': config.get('p4user'),
            'p4passwd': config.get('p4passwd'),
            'swarm_username': config.get('swarm_username'),
            'swarm_password': config.get('swarm_password'),
            'swarm_base_url': config.get('swarm_base_url', SWARM_BASE_URL),
            'swarm_api_url': config.get('swarm_api_url', SWARM_API_URL)
        }
    except Exception as e:
        print(f"读取配置文件出错: {str(e)}")
        return None

# 初始化默认配置
def init_default_config():
    global P4_DEFAULT_CLIENT, P4_DEFAULT_PORT, P4_DEFAULT_USER, P4_DEFAULT_PASSWD
    global SWARM_USERNAME, SWARM_PASSWORD, SWARM_BASE_URL, SWARM_API_URL
    
    # 从配置文件获取配置
    config_file_path = "p4config.json"
    if os.path.exists(config_file_path):
        file_config = read_p4_config_file(config_file_path)
        if file_config:
            P4_DEFAULT_CLIENT = file_config.get('p4client')
            P4_DEFAULT_PORT = file_config.get('p4port')
            P4_DEFAULT_USER = file_config.get('p4user')
            P4_DEFAULT_PASSWD = file_config.get('p4passwd')
            SWARM_USERNAME = file_config.get('swarm_username')
            SWARM_PASSWORD = file_config.get('swarm_password')
            if file_config.get('swarm_base_url'):
                SWARM_BASE_URL = file_config.get('swarm_base_url')
            if file_config.get('swarm_api_url'):
                SWARM_API_URL = file_config.get('swarm_api_url')

# 模拟浏览器登录获取cookie
def browser_login(username=None, password=None, base_url=None):
    """
    模拟浏览器登录P4Swarm，获取会话cookie
    
    Args:
        username: Swarm用户名
        password: Swarm密码
        base_url: Swarm基础URL
        
    Returns:
        requests.Session对象，包含登录后的cookie
    """
    # 使用全局配置或传入的参数
    username = username or SWARM_USERNAME
    password = password or SWARM_PASSWORD
    base_url = base_url or SWARM_BASE_URL
    
    if not username or not password:
        print("错误: 未提供Swarm用户名或密码")
        return None
    
    print(f"尝试模拟浏览器登录 {base_url}...")
    
    # 创建一个会话对象，用于保持cookie
    session = requests.Session()
    
    # 设置User-Agent头，模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    # 访问登录页面获取CSRF令牌
    try:
        print("访问登录页面...")
        login_url = "{}/login".format(base_url)
        response = session.get(login_url, headers=headers)
        
        if response.status_code != 200:
            print("访问登录页面失败，状态码: {}".format(response.status_code))
            return None
        
        # 解析HTML获取CSRF令牌
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = None
        
        # 查找CSRF令牌，通常在表单的隐藏输入字段中
        csrf_input = soup.find('input', {'name': 'csrf'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
        
        if not csrf_token:
            # 尝试从JavaScript中提取
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'csrf' in script.string:
                    match = re.search(r'csrf["\']?\s*:\s*["\']([^"\']+)["\']', script.string)
                    if match:
                        csrf_token = match.group(1)
                        break
        
        if not csrf_token:
            print("无法找到CSRF令牌")
            # 尝试继续，有些网站可能不需要CSRF令牌
        else:
            print("找到CSRF令牌: {}...".format(csrf_token[:10]))
        
        # 准备登录数据
        login_data = {
            'user': username,
            'password': password,
        }
        
        if csrf_token:
            login_data['csrf'] = csrf_token
        
        # 提交登录表单
        print("提交登录表单...")
        login_response = session.post(login_url, data=login_data, headers=headers, allow_redirects=True)
        
        # 检查登录是否成功
        if login_response.status_code == 200 or login_response.status_code == 302:
            # 检查是否有重定向到登录成功页面
            if 'dashboard' in login_response.url or 'home' in login_response.url:
                print("登录成功！")
            else:
                # 检查页面内容是否有登录成功的迹象
                if 'logout' in login_response.text.lower() or 'sign out' in login_response.text.lower():
                    print("登录成功！")
                else:
                    print("登录可能失败，请检查响应内容")
                    print("响应URL: {}".format(login_response.url))
                    # 打印部分响应内容以便调试
                    print("响应内容片段: {}...".format(login_response.text[:500]))
        else:
            print("登录失败，状态码: {}".format(login_response.status_code))
            return None
        
        # 打印cookie信息
        print("获取到的Cookie:")
        for cookie in session.cookies:
            print("  {}: {}".format(cookie.name, cookie.value))
        
        return session
        
    except Exception as e:
        print("模拟浏览器登录过程中发生错误: {}".format(e))
        return None

# 使用cookie创建API客户端
def create_api_client_with_cookies(session, api_url=None):
    """
    使用cookie创建API客户端
    
    Args:
        session: 包含cookie的会话对象
        api_url: Swarm API URL
        
    Returns:
        requests.Session对象，用于API调用
    """
    api_url = api_url or SWARM_API_URL
    
    try:
        # 创建一个新的请求会话，复制cookie
        api_session = requests.Session()
        api_session.cookies.update(session.cookies)
        
        # 测试API访问
        print("使用cookie测试API访问...")
        version_url = f"{api_url}/version"
        response = api_session.get(version_url)
        
        if response.status_code == 200:
            print(f"API访问成功！版本信息: {response.text}")
            return api_session
        else:
            print(f"API访问失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"创建API客户端时发生错误: {e}")
        return None

# 获取指定changelist的文件列表
def get_changelist_files(api_session, changelist_id, api_url=None):
    """
    获取指定changelist的文件列表
    
    Args:
        api_session: API会话对象
        changelist_id: 变更列表ID
        api_url: Swarm API URL
        
    Returns:
        包含文件列表的字典
    """
    api_url = api_url or SWARM_API_URL
    
    try:
        print(f"获取changelist {changelist_id}的文件列表...")
        
        # 构建API URL
        files_url = f"{api_url}/reviews/{changelist_id}/files"
        
        # 发送请求
        response = api_session.get(files_url)
        
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            
            # 检查是否有错误
            if data.get('error') is not None:
                print(f"获取文件列表失败，错误: {data.get('error')}")
                return None
            
            # 提取文件列表
            files_data = data.get('data', {})
            
            # 打印文件数量
            file_count = len(files_data)
            print(f"找到 {file_count} 个文件")
            
            return files_data
        else:
            print(f"获取文件列表失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"获取文件列表时发生错误: {e}")
        return None

# 获取文件差异
def get_file_diff(api_session, depot_file, revision, changelist_id, api_url=SWARM_API_URL):
    """
    获取文件差异
    
    Args:
        api_session: API会话对象
        depot_file: 文件路径
        revision: 文件版本
        changelist_id: 变更列表ID
        api_url: Swarm API URL
        
    Returns:
        包含文件差异的字典
    """
    try:
        print(f"获取文件差异: {depot_file}#{revision}")
        
        # 构建API URL
        diff_url = f"{api_url}/reviews/{changelist_id}/diff"
        
        # 准备请求参数
        params = {
            'path': depot_file,
            'version': revision,
            'context': 'all'  # 获取完整上下文
        }
        
        # 发送请求
        response = api_session.get(diff_url, params=params)
        
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            
            # 检查是否有错误
            if data.get('error') is not None:
                print(f"获取文件差异失败，错误: {data.get('error')}")
                return None
            
            # 提取差异数据
            diff_data = data.get('data', {})
            
            return diff_data
        else:
            print(f"获取文件差异失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"获取文件差异时发生错误: {e}")
        return None

# 获取文件完整内容
def get_file_complete_content(api_session, depot_file, changelist_id, api_url=SWARM_BASE_URL):
    """
    获取文件完整内容
    
    Args:
        api_session: API会话对象
        depot_file: 文件路径
        changelist_id: 变更列表ID
        api_url: Swarm基础URL
        
    Returns:
        文件内容字符串
    """
    try:
        print(f"获取文件完整内容: {depot_file}")
        
        # 构建URL
        file_url = f"{api_url}/reviews/{changelist_id}/file"
        
        # 准备请求参数
        params = {
            'path': depot_file
        }
        
        # 发送请求
        response = api_session.get(file_url, params=params)
        
        if response.status_code == 200:
            # 返回文件内容
            return response.text
        else:
            print(f"获取文件内容失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"获取文件内容时发生错误: {e}")
        return None

# 分析文件变更
def analyze_file_changes(diff_data):
    """
    分析文件变更
    
    Args:
        diff_data: 差异数据
        
    Returns:
        包含分析结果的字典
    """
    try:
        if not diff_data:
            return {"error": "没有差异数据"}
        
        # 提取差异块
        chunks = diff_data.get('chunks', [])
        
        # 初始化分析结果
        analysis = {
            "added_lines": 0,
            "deleted_lines": 0,
            "modified_lines": 0,
            "total_changes": 0,
            "chunks": len(chunks),
            "details": []
        }
        
        # 分析每个差异块
        for chunk in chunks:
            changes = chunk.get('changes', [])
            
            for change in changes:
                change_type = change.get('type')
                
                if change_type == 'add':
                    analysis["added_lines"] += 1
                elif change_type == 'remove':
                    analysis["deleted_lines"] += 1
                elif change_type == 'edit':
                    analysis["modified_lines"] += 1
                
                # 记录详细变更
                analysis["details"].append({
                    "type": change_type,
                    "line": change.get('line'),
                    "content": change.get('content')
                })
        
        # 计算总变更行数
        analysis["total_changes"] = analysis["added_lines"] + analysis["deleted_lines"] + analysis["modified_lines"]
        
        return analysis
        
    except Exception as e:
        print(f"分析文件变更时发生错误: {e}")
        return {"error": str(e)}

# MCP工具：获取变更列表文件目录
@mcp.tool()
async def get_changelist_files_catalog(changelist_id: int) -> str:
    """
    获取变更列表文件目录
    
    Args:
        changelist_id: 变更列表ID
        
    Returns:
        文件目录的JSON字符串
    """
    try:
        # 初始化配置
        init_default_config()
        
        # 检查配置
        if not SWARM_USERNAME or not SWARM_PASSWORD or not SWARM_BASE_URL or not SWARM_API_URL:
            return json.dumps({"error": "缺少Swarm配置，请检查配置文件"})
        
        # 登录获取cookie
        session = browser_login()
        if not session:
            return json.dumps({"error": "登录失败，无法获取cookie"})
        
        # 创建API客户端
        api_session = create_api_client_with_cookies(session)
        if not api_session:
            return json.dumps({"error": "创建API客户端失败"})
        
        # 获取文件列表
        files_data = get_changelist_files(api_session, changelist_id)
        if not files_data:
            return json.dumps({"error": "获取文件列表失败"})
        
        # 格式化结果
        result = {
            "changelist_id": changelist_id,
            "file_count": len(files_data),
            "files": []
        }
        
        # 处理文件数据
        for depot_file, file_info in files_data.items():
            result["files"].append({
                "path": depot_file,
                "action": file_info.get('action'),
                "type": file_info.get('type'),
                "revision": file_info.get('rev')
            })
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"获取变更列表文件目录时发生错误: {str(e)}"})

# MCP工具：获取文件详细信息
@mcp.tool()
async def get_file_details(action: str, file_path: str, revision: int, changelist_id: int) -> str:
    """
    获取文件详细信息
    
    Args:
        action: 文件操作类型（add, edit, delete等）
        file_path: 文件路径
        revision: 文件版本
        changelist_id: 变更列表ID
        
    Returns:
        文件详细信息的JSON字符串
    """
    try:
        # 初始化配置
        init_default_config()
        
        # 检查配置
        if not SWARM_USERNAME or not SWARM_PASSWORD or not SWARM_BASE_URL or not SWARM_API_URL:
            return json.dumps({"error": "缺少Swarm配置，请检查配置文件"})
        
        # 登录获取cookie
        session = browser_login()
        if not session:
            return json.dumps({"error": "登录失败，无法获取cookie"})
        
        # 创建API客户端
        api_session = create_api_client_with_cookies(session)
        if not api_session:
            return json.dumps({"error": "创建API客户端失败"})
        
        # 获取文件差异
        diff_data = get_file_diff(api_session, file_path, revision, changelist_id)
        
        # 分析文件变更
        analysis = analyze_file_changes(diff_data)
        
        # 返回分析结果
        return json.dumps(analysis, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"获取文件详细信息时发生错误: {str(e)}"})

# 分析文件
def analysis_file(analysis, file_path) -> str:
    """
    分析文件并生成报告
    
    Args:
        analysis: 分析结果
        file_path: 文件路径
        
    Returns:
        分析报告字符串
    """
    try:
        # 提取文件名
        file_name = os.path.basename(file_path)
        
        # 生成报告
        report = f"文件分析报告: {file_name}\n"
        report += f"路径: {file_path}\n"
        report += f"总变更行数: {analysis.get('total_changes', 0)}\n"
        report += f"添加行数: {analysis.get('added_lines', 0)}\n"
        report += f"删除行数: {analysis.get('deleted_lines', 0)}\n"
        report += f"修改行数: {analysis.get('modified_lines', 0)}\n"
        report += f"差异块数: {analysis.get('chunks', 0)}\n"
        
        # 添加详细变更
        report += "\n详细变更:\n"
        for detail in analysis.get('details', []):
            change_type = detail.get('type')
            line = detail.get('line')
            content = detail.get('content')
            
            if change_type == 'add':
                report += f"+ 行 {line}: {content}\n"
            elif change_type == 'remove':
                report += f"- 行 {line}: {content}\n"
            elif change_type == 'edit':
                report += f"* 行 {line}: {content}\n"
        
        return report
        
    except Exception as e:
        return f"生成分析报告时发生错误: {str(e)}"

# 初始化配置
init_default_config() 