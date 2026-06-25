from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithm_agent.agent import AlgorithmAgent
from quiz.generator import QuizGenerator
from quiz.scorer import QuizScorer

app = Flask(__name__)

# 初始化各个模块
algo_agent = AlgorithmAgent()
quiz_generator = QuizGenerator()
# 注意：实际项目中 scorer 应该按用户区分，这里简化为全局一个
scorers = {}  # user_id -> QuizScorer


@app.route('/api/algorithm/ask', methods=['POST'])
def ask_algorithm():
    """
    算法问答接口
    请求体: {"question": "K-means 原理是什么"}
    返回: {"answer": "..."}
    """
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': '问题不能为空'}), 400
    
    answer = algo_agent.answer(question)
    return jsonify({'answer': answer, 'agent': 'algorithm_agent'})


@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    """
    生成测验题目
    请求体: {
        "topic": "K-means",
        "difficulty": "easy",
        "num_questions": 5,
        "question_type": "choice"
    }
    """
    data = request.json
    topic = data.get('topic', '人工智能导论')
    difficulty = data.get('difficulty', 'medium')
    num_questions = data.get('num_questions', 5)
    question_type = data.get('question_type', 'choice')
    
    questions = quiz_generator.generate_questions(
        topic=topic,
        difficulty=difficulty,
        num_questions=num_questions,
        question_type=question_type
    )
    
    return jsonify({
        'topic': topic,
        'difficulty': difficulty,
        'questions': questions
    })


@app.route('/api/quiz/submit', methods=['POST'])
def submit_answer():
    """
    提交答案，获取评分
    请求体: {
        "user_id": "student1",
        "question": "题目内容",
        "user_answer": "A",
        "is_correct": true
    }
    """
    data = request.json
    user_id = data.get('user_id', 'default')
    question = data.get('question', '')
    user_answer = data.get('user_answer', '')
    is_correct = data.get('is_correct', False)
    
    # 获取或创建用户的评分器
    if user_id not in scorers:
        scorers[user_id] = QuizScorer()
    
    scorer = scorers[user_id]
    scorer.submit_answer(question, user_answer, is_correct)
    
    # 调整难度
    new_difficulty = scorer.adjust_difficulty()
    stats = scorer.get_stats()
    
    return jsonify({
        'is_correct': is_correct,
        'new_difficulty': new_difficulty,
        'stats': stats
    })


@app.route('/api/quiz/stats/<user_id>', methods=['GET'])
def get_stats(user_id):
    """获取用户的学习统计"""
    if user_id not in scorers:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify(scorers[user_id].get_stats())


if __name__ == '__main__':
    print("成员3 的 API 服务启动中...")
    print("端口: 5001")
    print("接口列表：")
    print("  POST /api/algorithm/ask   - 算法问答")
    print("  POST /api/quiz/generate   - 生成题目")
    print("  POST /api/quiz/submit     - 提交答案")
    print("  GET  /api/quiz/stats/<id> - 学习统计")
    app.run(port=5001, debug=True)