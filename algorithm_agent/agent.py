import ollama
import sys
import os

# 把项目根目录加入路径，方便导入 algorithms
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.kmeans import KMeans
from algorithms.knn import KNN
from algorithms.bfs_dfs import GraphSearch
from algorithms.neural_network import SimpleNeuralNetwork


class AlgorithmAgent:
    """
    算法 Agent：负责回答算法相关问题
    结合本地算法代码 + Ollama 大模型
    """
    
    def __init__(self, model_name='qwen2.5:7b'):
        self.model_name = model_name
        
        # 算法库：名字 → 算法类
        self.algorithms = {
            'kmeans': KMeans,
            'knn': KNN,
            'bfs': GraphSearch,
            'dfs': GraphSearch,
            '神经网络': SimpleNeuralNetwork,
            'neural network': SimpleNeuralNetwork,
        }
    
    def _detect_algorithm(self, question):
        """
        简单的关键词匹配，判断用户问的是哪个算法
        """
        question_lower = question.lower()
        
        if 'k-means' in question_lower or 'kmeans' in question_lower or '聚类' in question:
            return 'kmeans'
        elif 'knn' in question_lower or 'k近邻' in question or '最近邻' in question:
            return 'knn'
        elif 'bfs' in question_lower or '广度优先' in question:
            return 'bfs'
        elif 'dfs' in question_lower or '深度优先' in question:
            return 'dfs'
        elif '神经网络' in question or 'neural network' in question_lower:
            return '神经网络'
        else:
            return None
    
    def _get_algorithm_code(self, algo_name):
        """读取算法文件的源代码"""
        file_map = {
            'kmeans': 'algorithms/kmeans.py',
            'knn': 'algorithms/knn.py',
            'bfs': 'algorithms/bfs_dfs.py',
            'dfs': 'algorithms/bfs_dfs.py',
            '神经网络': 'algorithms/neural_network.py',
        }
        
        if algo_name in file_map:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                file_map[algo_name]
            )
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
        
    def answer(self, question):
        """
        回答用户的算法问题
        流程：
        1. 识别用户问的是哪个算法
        2. 把算法代码和问题一起发给大模型
        3. 让大模型结合代码来回答
        """
        
        algo_name = self._detect_algorithm(question)
        
        if algo_name:
            # 找到对应算法，把算法代码也给大模型参考
            code = self._get_algorithm_code(algo_name)
            
            system_prompt = f"""
            你是人工智能导论课程的算法老师。
            学生问你关于 {algo_name} 算法的问题。
            
            这里有一份该算法的 Python 实现代码：
            ```python
            {code}
请你：
用通俗易懂的语言回答问题
必要时引用代码片段来说明
讲解要清晰，适合大一学生理解
如果涉及原理，先讲直觉再讲细节
            """
        else:
            system_prompt = """
你是人工智能导论课程的算法老师。
请用通俗易懂的语言回答学生的问题，适合大一学生理解。
尽量结合代码和例子来讲解。
            """
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': question}
            ]
        )
        return response['message']['content']
if __name__ == "__main__":
    agent = AlgorithmAgent()
    print("=== 算法 Agent 测试 ===")
    print("输入你的问题，输入 'quit' 退出 \n")
    while True:
        question = input("你:")
        if question.lower() == 'quit':
            break
        print("\n算法老师:", end="", flush=True)
        answer = agent.answer(question)
        print(answer)
        print("-" * 50)