# AI导学系统 - 后端API接口文档

## 基础信息
- 服务器地址：http://localhost:5000
- 数据格式：JSON
- 字符编码：UTF-8

---

## 接口列表

### 1. 健康检查
**接口地址**：`GET /api/health`

**功能说明**：检查后端服务是否正常运行

**请求参数**：无

**返回示例**：
```json
{
  "status": "ok",
  "message": "AI导学系统运行正常！",
  "knowledge_count": 6,
  "question_count": 30
}
```

**返回字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| status | string | 状态：ok表示正常 |
| message | string | 状态描述 |
| knowledge_count | number | 知识库知识点数量 |
| question_count | number | 题库题目数量 |

---

### 2. 获取知识库列表
**接口地址**：`GET /api/knowledge`

**功能说明**：获取所有知识点的列表

**请求参数**：无

**返回示例**：
```json
{
  "knowledge": [
    {"id": "cnn", "name": "cnn"},
    {"id": "gradient_descent", "name": "gradient_descent"},
    {"id": "kmeans", "name": "kmeans"},
    {"id": "knn", "name": "knn"},
    {"id": "linear_regression", "name": "linear_regression"},
    {"id": "transformer", "name": "transformer"}
  ]
}
```

**返回字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| knowledge | array | 知识点列表 |
| id | string | 知识点ID |
| name | string | 知识点名称 |

---

### 3. 聊天接口（主接口）
**接口地址**：`POST /api/chat`

**功能说明**：用户提问，AI自动选择合适的Agent回答

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| question | string | 是 | 用户的问题 |

**请求示例**：
```json
{
  "question": "什么是K-means算法？"
}
```

**返回示例**：
```json
{
  "answer": "【概念讲解Agent】\nK-means是一种无监督聚类算法...",
  "agent": "概念讲解Agent",
  "question": "什么是K-means算法？",
  "knowledge_used": "\n\n参考课程资料：\n【kmeans】..."
}
```

**返回字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| answer | string | AI的回答内容 |
| agent | string | 使用的Agent名称 |
| question | string | 用户的问题（原样返回） |
| knowledge_used | string | 检索到的知识库内容 |

---

### 4. 抽取测验题目
**接口地址**：`POST /api/quiz/get`

**功能说明**：从题库中随机抽取一道题目

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| concept | string | 否 | 指定知识点，如 kmeans、knn 等 |
| difficulty | string | 否 | 难度：easy / medium / hard |

**请求示例1（随机抽题）**：
```json
{}
```

**请求示例2（指定知识点）**：
```json
{
  "concept": "kmeans"
}
```

**返回示例**：
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "concept": "kmeans",
    "question": "K-means属于什么类型的算法？",
    "options": ["监督学习", "无监督学习", "强化学习", "半监督学习"]
  }
}
```

**返回字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | number | 状态码：200成功，404没有题目 |
| data | object | 题目数据 |
| id | number | 题目ID |
| concept | string | 所属知识点 |
| question | string | 题目内容 |
| options | array | 选项（选择题有，填空题可能没有） |

---

### 5. 提交答案判分
**接口地址**：`POST /api/quiz/submit`

**功能说明**：提交用户答案，自动判分并给出解析

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_answer | string | 是 | 用户的答案 |

**请求示例**：
```json
{
  "user_answer": "无监督学习"
}
```

**返回示例（答对）**：
```json
{
  "code": 200,
  "data": {
    "is_correct": true,
    "correct_answer": "无监督学习",
    "explanation": "K-means是聚类算法，属于无监督学习..."
  }
}
```

**返回示例（答错）**：
```json
{
  "code": 200,
  "data": {
    "is_correct": false,
    "correct_answer": "无监督学习",
    "explanation": "K-means是聚类算法，属于无监督学习..."
  }
}
```

**返回字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | number | 状态码：200成功，400没有正在做的题 |
| data | object | 判分结果 |
| is_correct | boolean | 是否答对 |
| correct_answer | string | 正确答案 |
| explanation | string | 答案解析 |

---

### 6. 获取错题本
**接口地址**：`GET /api/quiz/error`

**功能说明**：查看所有做错的题目

**请求参数**：无

**返回示例**：
```json
{
  "code": 200,
  "count": 2,
  "data": [
    {
      "id": 1,
      "concept": "kmeans",
      "question": "K-means属于什么类型的算法？",
      "options": ["监督学习", "无监督学习", "强化学习", "半监督学习"],
      "answer": "无监督学习",
      "explanation": "K-means是聚类算法..."
    }
  ]
}
```

**返回字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | number | 状态码：200成功 |
| count | number | 错题数量 |
| data | array | 错题列表 |

---

## Agent说明

系统会根据用户问题自动选择最合适的Agent：

| Agent名称 | 触发关键词 | 功能 |
|----------|-----------|------|
| 概念讲解Agent | 默认 | 解释基础概念，大白话+生活例子 |
| 数学推导Agent | 推导、证明、为什么、数学、原理 | 分步骤讲解数学原理 |
| 算法代码Agent | 代码、python、实现、编程 | 提供完整Python代码和注释 |
| 测验生成Agent | 测验、做题、考试、出题、刷题 | 生成测验题目和解析 |

---

## 注意事项

1. 后端服务需要一直保持运行
2. Ollama服务也需要启动
3. 确保模型 `gemma3:4b` 已下载
4. 所有接口请求和返回都是 JSON 格式
5. 字符编码统一使用 UTF-8

---

## 更新记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-06-20 | 初始版本，完成基础接口 |