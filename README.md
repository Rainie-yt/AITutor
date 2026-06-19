markdown
# 🤖 AI导学系统（多智能体）

> 人工智能导论课程项目 - 基于多Agent架构的智能导学系统

---

## 📋 项目简介

AI导学系统是一个面向大学生的人工智能课程学习助手，采用多智能体架构，能够根据用户问题自动选择最合适的AI老师进行解答，支持概念讲解、数学推导、代码实现、在线测验等多种功能。

---

## ✨ 功能特性

### 🧠 多智能体系统
- **概念讲解Agent**：用大白话解释基础概念，结合生活例子，通俗易懂
- **数学推导Agent**：分步骤讲解数学原理，适合大一学生理解
- **算法代码Agent**：提供完整可运行的Python代码，关键行加注释
- **测验生成Agent**：自动生成测验题目，支持判分和错题本

### 📚 RAG知识库检索
- 基于课程资料的知识库
- 关键词智能匹配
- 自动注入相关知识，回答更准确

### 📝 在线测验系统
- 按知识点抽题
- 难度分级
- 自动判分和详细解析
- 错题本功能，方便复习

---

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 后端框架 | Flask 3.0 |
| 大模型 | Ollama + gemma3:4b |
| 知识库 | Markdown + RAG检索 |
| 前端 | （待补充） |
| 接口风格 | RESTful API |

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Ollama（需下载 gemma3:4b 模型）

### 安装步骤

1. **克隆项目**
```bash
git clone 项目地址
cd AI导学后端
```

2. **安装依赖**
```bash
pip install flask flask-cors ollama requests
```

3. **下载模型**
```bash
ollama pull gemma3:4b
```

4. **启动后端服务**
```bash
python app_chat.py
```

5. **访问测试**
```bash
健康检查：http://localhost:5000/api/health
接口文档：见 API接口文档.md
```

---

## 📁 项目结构
```bash
plaintext
AI导学后端/
├── app_chat.py              # 后端主程序
├── API接口文档.md           # API接口文档
├── README.md                # 项目说明
├── requirements.txt         # Python依赖列表
├── venv/                    # Python虚拟环境
└── knowledge_base/          # 知识库目录
    ├── knowledge_docs/      # 知识点Markdown文件
    │   ├── cnn.md
    │   ├── gradient_descent.md
    │   ├── kmeans.md
    │   ├── knn.md
    │   ├── linear_regression.md
    │   └── transformer.md
    ├── knowledge_graph.json # 知识图谱数据
    └── question_bank.json   # 测验题库
```

---

## 📖 API 接口
详细接口文档请查看：API 接口文档.md

### 主要接口

| 接口 | 方法 | 功能 |
|------|------|------|
| /api/health | GET | 健康检查 |
| /api/knowledge | GET | 获取知识库列表 |
| /api/chat | POST | 聊天问答 |
| /api/quiz/get | POST | 抽取测验题目 |
| /api/quiz/submit | POST | 提交答案判分 |
| /api/quiz/error | GET | 获取错题本 |

---

## 👥 团队成员

| 成员 | 角色 | 负责模块 |
|------|------|------|
| 成员一 | 后端主程 | Flask 后端、Agent 调度、Ollama 集成、API 接口 |
| 成员二 | 知识库负责人 | 课程资料整理、知识图谱构建、Prompt 优化 |
| 成员三 | 算法负责人 | 经典算法实现、测验生成模块 |
| 成员四 | 前端负责人 | 聊天界面、可视化、项目 PPT |

---

## 📅 项目进度

- ✅ 环境配置完成
- ✅ Flask 后端框架搭建
- ✅ Ollama 大模型集成
- ✅ 多 Agent 调度系统
- ✅ RAG 知识库检索
- ✅ 在线测验系统
- ✅ API 接口文档
- 🔄 前后端联调（进行中）
- ⏳ 前端页面开发
- ⏳ 系统测试优化

---

## 📝 更新日志
- v1.0.0 (2026-06-20)
- 完成基础后端框架
- 实现 4 个 AI Agent
- 集成 RAG 知识库检索
- 实现在线测验系统
- 完成 API 接口文档

---

## 🙏 致谢
- 感谢所有为项目做出贡献的同学！
- 感谢《人工智能导论》课程老师的指导！

---