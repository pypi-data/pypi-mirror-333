# mcp-perforce 工具

这是一个用于与 Perforce Swarm 系统交互的工具，提供了查看变更列表、获取文件详细变更等功能。

## 功能特性

- 根据review的cl号获取变更文件目录
- 根据文件从swarm获取详细变更记录

## 使用方法
```
mcp-perforce --p4config p4config.json
```

p4config.json
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