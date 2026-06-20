import ollama
import json


class QuizGenerator:
    """
    测验生成模块：调用 Ollama 自动生成题目
    支持三种难度：简单、中等、困难
    支持三种题型：选择题、判断题、简答题
    """
    
    def __init__(self, model_name='qwen2.5:7b'):
        self.model_name = model_name
    
    def generate_questions(self, topic, difficulty='medium', num_questions=5, question_type='choice'):
        """
        生成题目
        
        参数：
        - topic: 主题，比如 "K-means 聚类"
        - difficulty: 难度 easy/medium/hard
        - num_questions: 题目数量
        - question_type: 题型 choice(选择)/judge(判断)/short(简答)
        
        返回：题目列表，每个题目是字典
        """
        
        # 根据题型构造不同的 prompt
        if question_type == 'choice':
            format_instruction = """
            请生成选择题，每题包含：
            - question: 题目内容
            - options: 四个选项的列表 [A, B, C, D]
            - answer: 正确答案的字母
            - explanation: 答案解析
            
            严格按照 JSON 数组格式返回，不要有其他文字。
            示例格式：
            [
              {
                "question": "以下哪个是监督学习？",
                "options": ["K-means", "KNN", "PCA", "DBSCAN"],
                "answer": "B",
                "explanation": "KNN 是监督学习分类算法，需要标签数据。"
              }
            ]
            """
        elif question_type == 'judge':
            format_instruction = """
            请生成判断题，每题包含：
            - question: 题目内容
            - answer: true 或 false
            - explanation: 答案解析
            
            严格按照 JSON 数组格式返回。
            """
        else:  # short answer
            format_instruction = """
            请生成简答题，每题包含：
            - question: 题目内容
            - answer: 参考答案要点
            - explanation: 详细解答思路
            
            严格按照 JSON 数组格式返回。
            """
        
        difficulty_desc = {
            'easy': '基础概念题，考察基本定义和简单理解',
            'medium': '中等难度，考察原理理解和简单应用',
            'hard': '较难，考察深入理解和综合应用'
        }
        
        prompt = f"""
        你是人工智能导论课程的出题老师。
        请围绕 "{topic}" 这个知识点，出 {num_questions} 道 {difficulty_desc[difficulty]} 的题目。
        
        {format_instruction}
        
        注意：
        1. 题目要准确，不能有错误
        2. 解析要清晰，帮助学生理解
        3. 只返回 JSON，不要任何额外文字
        """
        
        # 调用 Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        
        # 解析返回的 JSON
        try:
            # 有时候大模型会返回 ```json ... ``` 包裹，需要处理
            content = response['message']['content']
            # 去掉可能的 markdown 代码块标记
            content = content.replace('```json', '').replace('```', '').strip()
            questions = json.loads(content)
            return questions
        except json.JSONDecodeError as e:
            print(f"解析题目失败: {e}")
            print("大模型返回的内容：")
            print(response['message']['content'])
            return []


# 测试
if __name__ == "__main__":
    generator = QuizGenerator()
    
    print("生成 K-means 相关的选择题（简单难度）...")
    questions = generator.generate_questions(
        topic="K-means 聚类算法",
        difficulty="easy",
        num_questions=3,
        question_type="choice"
    )
    
    for i, q in enumerate(questions, 1):
        print(f"\n第 {i} 题：{q['question']}")
        for opt in q['options']:
            print(f"  {opt}")
        print(f"答案：{q['answer']}")
        print(f"解析：{q['explanation']}")