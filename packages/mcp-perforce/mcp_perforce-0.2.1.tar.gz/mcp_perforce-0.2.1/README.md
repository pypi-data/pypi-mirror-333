# MCP Perforce 服务器

Perforce的模型上下文协议(MCP)服务器实现

## 功能概述

MCP Perforce服务器提供了一个简单的获取reviews目录，以及目录中每个变更文件详细内容

## 使用说明
cursor MCP 配置说明
```json
{
    "mcpServers": {
      "code review": {
          "command": "uvx",
          "args": [
              "mcp-perforce",
              "--p4config",
              "./mcp-servers/perforce_service/p4config.json"
          ]
      }
  }      
}  
```

p4config.json说明

```json
{
  "swarm_username": "your_swarm_username",
  "swarm_password": "your_swarm_password",
  "swarm_base_url": "https://your_swarm_server",
  "swarm_api_url": "https://your_swarm_server/api/v10"
}
```