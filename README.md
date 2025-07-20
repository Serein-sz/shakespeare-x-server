# document-x-server
 
 文档编写网站
 
 ## 项目简介
 
 这是一个基于Python的文档编写网站，提供创建、编辑和管理文档的功能。
 
 ## 功能特性
 
 - 在线文档编辑
 - 版本控制
 - 协作编写
 - Markdown支持
 
 ## 安装要求
 
 - Python 3.10+
 - UV包管理器
 
 ## 安装方法
 
 ```bash
 uv sync
 ```
 
 ## 使用说明

默认启动命令已包含以下配置：
- `--host 0.0.0.0`: 允许远程访问
- `--port 8000`: 指定服务端口
- `--timeout-keep-alive 300`: 设置keep-alive超时时间为300秒
 
 1. 启动服务：
 ```bash
 uvicorn main.py --host 0.0.0.0 --port 8000 --timeout-keep-alive 300
 ```
 
 2. 访问网站：`http://localhost:8000`
 
 ## 开发
 
 ```bash
 # 运行测试
 pytest
 ```

## 贡献

欢迎提交Pull Request或Issue。

## 许可证

MIT