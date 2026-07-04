"""
AI导学系统 - 后端主程序
功能：多Agent智能问答 + RAG知识库 + 测验系统
作者：AI导学项目组
"""

from flask import Flask, request, jsonify
import ollama
import os
import glob
import json
import random

# 初始化Flask应用
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)  # 允许所有来源跨域访问
app.config['JSON_AS_ASCII'] = False
# 对话历史存储（key: 用户ID, value: 历史消息列表）
chat_history = {}

# ==========================================
# 一、知识库模块（RAG检索增强生成）
# ==========================================

def load_knowledge():
    """
    加载知识库：从knowledge_docs文件夹读取所有md文件
    返回：字典格式的知识库
    """
    knowledge = {}
    # 查找所有md文件
    md_files = glob.glob('knowledge_base/knowledge_docs/*.md')
    
    for file_path in md_files:
        # 提取文件名（去掉.md后缀）作为知识点ID
        filename = os.path.basename(file_path).replace('.md', '')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                knowledge[filename] = {
                    'name': filename,      # 知识点名称
                    'content': content,    # 知识点详细内容
                    'keywords': [filename] # 关键词（用于匹配）
                }
        except Exception as e:
            print(f"加载文件 {filename} 失败：{e}")
    
    return knowledge

# 全局知识库变量
knowledge_base = load_knowledge()

# ==========================================
# 二、题库模块（测验系统）
# ==========================================

def load_question_bank():
    """
    加载题库：从question_bank.json读取
    返回：题目列表
    """
    try:
        with open('knowledge_base/question_bank.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"题库加载失败：{e}")
        return []

# 全局题库变量
question_bank = load_question_bank()
error_book = []          # 错题本（内存存储，重启清空）
current_quiz = None      # 当前正在作答的题目

# ==========================================
# 三、RAG检索模块
# ==========================================

def search_knowledge(question):
    """
    根据用户问题检索相关知识库内容
    参数：question - 用户问题
    返回：格式化的参考资料字符串
    """
    q = question.lower()
    results = []
    
    for key, item in knowledge_base.items():
        # 方式1：按文件名匹配
        if key.lower() in q:
            results.append(f"【{item['name']}】\n{item['content'][:500]}...")
            continue
        # 方式2：按内容关键词匹配
        if q in item['content'].lower():
            results.append(f"【{item['name']}】\n{item['content'][:500]}...")
    
    if results:
        return "\n\n参考课程资料：\n" + "\n".join(results)
    return "\n\n参考课程资料：暂无相关内容"

# ==========================================
# 四、Agent人设模块
# ==========================================

# 数学推导Agent
MATH_PROMPT = """
你是【数学推导Agent】，专门讲人工智能里的数学原理。
要求：
1. 用通俗易懂的话，适合大一学生
2. 分步骤讲解
3. 开头一定要写【数学推导Agent】
4. 请结合下面的课程资料回答

用户问题：{q}
{knowledge}
"""

# 算法代码Agent
CODE_PROMPT = """
你是【算法代码Agent】，专门给Python代码和讲解。
要求：
1. 给完整可运行的代码
2. 关键行加注释
3. 开头一定要写【算法代码Agent】
4. 请结合下面的课程资料回答

用户问题：{q}
{knowledge}
"""

# 概念讲解Agent
CONCEPT_PROMPT = """
你是【概念讲解Agent】，专门解释基础概念。
要求：
1. 用大白话讲
2. 举生活中的例子
3. 开头一定要写【概念讲解Agent】
4. 请结合下面的课程资料回答

用户问题：{q}
{knowledge}
"""

# 测验生成Agent
QUIZ_PROMPT = """
你是【测验生成Agent】，专门帮学生出题和讲解题目。
要求：
1. 开头一定要写【测验生成Agent】
2. 先给出题目，再给出答案和详细解析
3. 适合大一学生的难度

用户要求：{q}
参考题库：{knowledge}
"""

# ==========================================
# 五、Agent调度模块
# ==========================================

def choose_agent(question):
    """
    根据用户问题自动选择最合适的Agent
    参数：question - 用户问题
    返回：(prompt模板, agent名称)
    """
    q = question.lower()
    
    # 1. 测验意图
    quiz_words = ['测验', '做题', '考试', '出题', '刷题', '测试', '考考我']
    if any(w in q for w in quiz_words):
        return QUIZ_PROMPT, "测验生成Agent"
    
    # 2. 数学推导意图
    math_words = ['推导', '证明', '为什么', '数学', '原理', '收敛', '导数', '公式']
    if any(w in q for w in math_words):
        return MATH_PROMPT, "数学推导Agent"
    
    # 3. 代码实现意图
    code_words = ['代码', 'python', '实现', '怎么写', '编程', '程序']
    if any(w in q for w in code_words):
        return CODE_PROMPT, "算法代码Agent"
    
    # 4. 默认：概念讲解
    return CONCEPT_PROMPT, "概念讲解Agent"

# ==========================================
# 六、API接口
# ==========================================

@app.route('/api/health', methods=['GET'])
def health():
    """
    健康检查接口
    返回：系统状态、知识库数量、题库数量
    """
    return jsonify(
        status="ok", 
        message="AI导学系统运行正常！",
        knowledge_count=len(knowledge_base),
        question_count=len(question_bank)
    )

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """
    获取知识库列表
    返回：所有知识点的ID和名称
    """
    result = []
    for key, item in knowledge_base.items():
        result.append({"id": key, "name": item['name']})
    return jsonify(knowledge=result)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get('question', '')
        user_id = data.get('user_id', 'default')
        
        if not question:
            return jsonify({"code": 400, "msg": "问题不能为空"}), 400
        
        # 1. 检索知识库
        knowledge = search_knowledge(question)
        
        # 2. 自动选择Agent
        prompt_template, agent_name = choose_agent(question)
        
        # 3. 拼接历史对话
        history_text = ""
        if user_id in chat_history:
            recent_history = chat_history[user_id][-10:]
            for msg in recent_history:
                if msg['role'] == 'user':
                    history_text += f"用户：{msg['content']}\n"
                else:
                    history_text += f"AI：{msg['content']}\n"
        
        # 4. 构造prompt
        prompt = prompt_template.format(q=question, knowledge=knowledge)
        if history_text:
            prompt = f"之前的对话历史：\n{history_text}\n\n" + prompt
        
        # 5. 调用大模型
        print(f"[{agent_name}] 用户提问：{question}")
        response = ollama.generate(model='gemma3:4b', prompt=prompt)
        answer = response['response']
        
        # 6. 保存对话历史
        if user_id not in chat_history:
            chat_history[user_id] = []
        chat_history[user_id].append({'role': 'user', 'content': question})
        chat_history[user_id].append({'role': 'assistant', 'content': answer})
        
        print(f"[{agent_name}] 回答完成，长度：{len(answer)}")
        
        return jsonify(
            answer=answer,
            agent=agent_name,
            question=question,
            knowledge_used=knowledge,
            history_count=len(chat_history[user_id]) // 2
        )
    
    except Exception as e:
        print(f"聊天接口出错：{e}")
        return jsonify({
            "code": 500,
            "msg": f"服务器出错：{str(e)}"
        }), 500

@app.route('/api/chat/clear', methods=['POST'])
def clear_history():
    """清空对话历史"""
    data = request.get_json()
    user_id = data.get('user_id', 'default')
    
    if user_id in chat_history:
        del chat_history[user_id]
    
    return jsonify({"code": 200, "message": "对话历史已清空"})

    # 知识图谱接口
@app.route('/api/knowledge_graph', methods=['GET'])
def get_knowledge_graph():
    """获取知识图谱数据（自动提取节点并拼接知识库内容）"""
    try:
        with open('knowledge_base/knowledge_graph.json', 'r', encoding='utf-8') as f:
            edges = json.load(f)
        
        # 1. 从所有边中提取所有节点（去重）
        node_names = set()
        for edge in edges:
            node_names.add(edge.get('source', ''))
            node_names.add(edge.get('target', ''))
        
        # 2. 构造节点列表，拼接知识库内容
        nodes = []
        for name in node_names:
            node = {
                'id': name,
                'name': name
            }
            # 去知识库里找有没有这个知识点（模糊匹配）
            for key, item in knowledge_base.items():
                if key.lower() in name.lower() or name.lower() in key.lower():
                    node['content'] = item.get('content', '')
                    node['keywords'] = item.get('keywords', [])
                    break
            nodes.append(node)
        
        # 3. 返回标准的 nodes + edges 格式
        return jsonify({
            "code": 200,
            "data": {
                "nodes": nodes,
                "edges": edges
            }
        })
    except Exception as e:
        print(f"加载知识图谱失败：{e}")
        return jsonify({
            "code": 500,
            "msg": f"加载知识图谱失败：{str(e)}"
        }), 500

# ==========================================
# 七、测验相关接口
# ==========================================

@app.route('/api/quiz/get', methods=["GET", "POST"])
def get_quiz():
    try:
        global current_quiz
        
        # 支持GET和POST两种方式
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args
        
        concept = data.get('concept', '')
        difficulty = data.get('difficulty', '')
        
        candidates = question_bank
        
        if concept:
            # 模糊匹配：不区分大小写，去掉连字符和空格
            concept_norm = concept.lower().replace('-', '').replace(' ', '')
            candidates = [q for q in candidates if concept_norm in q.get('concept', '').lower().replace('-', '').replace(' ', '')]
        
        if difficulty:
            candidates = [q for q in candidates if q.get('difficulty', '') == difficulty]
        
        if not candidates:
            return jsonify({"question": "暂无符合条件的题目", "options": []}), 404
        
        selected = random.choice(candidates)
        current_quiz = selected
        
        # 返回前端期望的格式
        return jsonify({
            "question": selected.get("question", ""),
            "options": selected.get("options", []),
            "id": selected.get("id"),
            "concept": selected.get("concept"),
            "type":selected.get("type", "choice")
        })
    except Exception as e:
        print(f"抽题接口出错：{e}")
        return jsonify({"question": "服务器出错", "options": []}), 500

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    提交答案并判分
    请求参数：user_answer - 用户答案
    返回：是否正确、正确答案、解析
    """
    global current_quiz
    if not current_quiz:
        return jsonify({"code": 400, "msg": "暂无正在作答的题目，请先获取题目"}), 400
    
    data = request.get_json()
    user_ans = data.get('user_answer', '').strip()
    correct_ans = current_quiz.get('answer', '')
    is_right = (user_ans == correct_ans)
    
    # 答错加入错题本
    if not is_right and current_quiz not in error_book:
        error_book.append(current_quiz)
    
    result = {
        "code": 200,
        "data": {
            "is_correct": is_right,
            "correct_answer": correct_ans,
            "explanation": current_quiz.get('explanation', '暂无解析')
        }
    }
    current_quiz = None
    return jsonify(result)

@app.route('/api/quiz/error', methods=['GET'])
def get_error_book():
    """获取错题本"""
    return jsonify({
        "code": 200,
        "count": len(error_book),
        "data": error_book
    })

@app.route('/api/quiz/clear', methods=['POST'])
def clear_error_book():
    """清空错题本"""
    try:
        global error_book
        error_book = []
        return jsonify({
            "code": 200,
            "message": "错题本已清空"
        })
    except Exception as e:
        print(f"清空错题本失败：{e}")
        return jsonify({
            "code": 500,
            "msg": str(e)
        }), 500


@app.route('/api/quiz/remove', methods=['POST'])
def remove_error():
    """从错题本移除某道题"""
    try:
        global error_book
        data = request.get_json()
        question_id = data.get('id', '')
        
        # 按id移除对应的题目
        error_book = [q for q in error_book if str(q.get('id')) != str(question_id)]
        
        return jsonify({
            "code": 200,
            "message": "已从错题本移除",
            "count": len(error_book)
        })
    except Exception as e:
        print(f"移除错题失败：{e}")
        return jsonify({
            "code": 500,
            "msg": str(e)
        }), 500

# ==========================================
# 启动服务
# ==========================================
if __name__ == '__main__':
    print("="*60)
    print("  🚀 AI导学系统 - 后端启动成功！")
    print("="*60)
    print(f"  📚 知识库：{len(knowledge_base)} 个知识点")
    print(f"  📝 题库：{len(question_bank)} 道题目")
    print(f"  🤖 大模型：gemma3:4b")
    print("="*60)
    print("  健康检查：http://localhost:5000/api/health")
    print("  聊天接口：http://localhost:5000/api/chat")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)