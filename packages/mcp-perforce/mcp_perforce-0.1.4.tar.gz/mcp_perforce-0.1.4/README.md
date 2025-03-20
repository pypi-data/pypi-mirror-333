# mcp-perforce 工具

这是一个用于与 Perforce Swarm 系统交互的工具，提供了查看变更列表、获取文件详细变更等功能。

## 功能特性

- 根据review的cl号获取变更文件目录
- 根据文件从swarm获取详细变更记录
- 分析文件变更内容，生成变更报告

## 安装方法

### 从PyPI安装

```bash
pip install mcp-perforce
```

### 从源码安装

```bash
git clone https://github.com/yourusername/mcp-perforce.git
cd mcp-perforce
pip install -e .
```

## 使用方法

### 配置文件

首先，创建一个`p4config.json`配置文件：

```json
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
```

### 命令行使用

启动MCP服务器：

```bash
mcp-perforce --p4config p4config.json --serve
```

查看版本信息：

```bash
mcp-perforce --version
```

### 作为库使用

```python
from mcp_perforce.perforce import get_changelist_files_catalog, get_file_details

# 获取变更列表文件目录
files_catalog = await get_changelist_files_catalog(12345)
print(files_catalog)

# 获取文件详细信息
file_details = await get_file_details("edit", "//depot/path/to/file.txt", 1, 12345)
print(file_details)
```

## 开发指南

### 环境设置

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .
```

### 构建和发布

```bash
# 构建包
python -m build

# 发布到PyPI
twine upload dist/*
```

## 许可证

MIT

## 贡献指南

欢迎提交问题和拉取请求！