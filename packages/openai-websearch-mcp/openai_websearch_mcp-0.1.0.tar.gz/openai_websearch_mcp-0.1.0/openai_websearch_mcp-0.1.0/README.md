# OpenAI WebSearch MCP

一个使用FastMCP框架的模型控制协议(MCP)服务器，旨在将OpenAI的网络搜索功能集成到Claude等不具备网络搜索能力的AI模型中。

## 项目概述

OpenAI WebSearch MCP利用OpenAI的`web_search_preview`工具，使其他AI模型（如Claude）能够执行网络搜索并在回答中利用最新的网络信息。该项目通过FastMCP框架实现，提供了一个简单的API，可以轻松集成到现有的AI工作流程中。

## 功能特点

- 通过MCP协议为Claude等AI模型提供网络搜索能力
- 利用OpenAI的网络搜索API获取实时网络信息
- 支持自定义搜索参数和用户位置设置
- 基于FastMCP框架，易于扩展和维护

## 安装

本项目使用`uv`进行包管理，确保您已安装了Python和uv。

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/openai-websearch-mcp.git
   cd openai-websearch-mcp
   ```

2. 安装依赖：
   ```bash
   uv sync --frozen
   ```

## 配置

1. 设置OpenAI API密钥：
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## 使用方法

### 启动MCP服务器测试

```bash
fastmcp run main.py

# Or run with inspector
fastmcp dev main.py
```

服务器默认在`localhost:5173`启动。

### 在客户端中使用

在与Claude或其他AI模型的交互中使用MCP客户端调用网络搜索功能：

```python
fastmcp install server.py -e API_KEY=your-api-key
```

## API参考

### 网络搜索工具属性

- `type`: 搜索工具类型，始终为`web_search_preview`
- `search_context_size`: 搜索上下文窗口大小，可选值为"low"、"medium"、"high"，默认为"medium"
- `user_location`: 用户位置参数（可选）
  - `type`: 位置近似类型，始终为"approximate"
  - `city`: 用户所在城市，例如"Shanghai"
  - `country`: 用户所在国家的两字母ISO代码，例如"CN"
  - `region`: 用户所在地区，例如"Shanghai"
  - `timezone`: 用户IANA时区，例如"Asia/Shanghai"


## 许可证

[MIT License](LICENSE)

## 贡献

欢迎贡献代码、报告问题或提出改进建议！请fork本仓库并提交拉取请求。
