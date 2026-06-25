class QuizScorer:
    """
    评分与难度调整模块
    根据学生的答题正确率，动态调整下一次的题目难度
    """
    
    def __init__(self):
        # 记录答题历史
        self.history = []
        # 当前难度
        self.current_difficulty = 'easy'
        # 难度等级
        self.difficulty_levels = ['easy', 'medium', 'hard']
    
    def submit_answer(self, question, user_answer, is_correct):
        """
        提交一次答题结果
        
        参数：
        - question: 题目内容
        - user_answer: 用户的答案
        - is_correct: 是否正确（布尔值）
        """
        self.history.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'difficulty': self.current_difficulty
        })
    
    def get_accuracy(self, last_n=None):
        """
        计算正确率
        last_n: 只计算最近 n 题，None 表示全部
        """
        if not self.history:
            return 0
        
        if last_n:
            recent = self.history[-last_n:]
        else:
            recent = self.history
        
        correct = sum(1 for h in recent if h['is_correct'])
        return correct / len(recent)
    
    def adjust_difficulty(self):
        """
        根据最近 5 题的正确率调整难度
        
        规则：
        - 正确率 >= 80% → 难度提升一级
        - 正确率 <= 40% → 难度降低一级
        - 中间 → 保持不变
        """
        if len(self.history) < 5:
            return self.current_difficulty  # 题太少，不调整
        
        accuracy = self.get_accuracy(last_n=5)
        current_idx = self.difficulty_levels.index(self.current_difficulty)
        
        if accuracy >= 0.8 and current_idx < len(self.difficulty_levels) - 1:
            # 正确率高，升级
            self.current_difficulty = self.difficulty_levels[current_idx + 1]
            print(f"正确率 {accuracy:.0%}，难度提升为：{self.current_difficulty}")
        elif accuracy <= 0.4 and current_idx > 0:
            # 正确率低，降级
            self.current_difficulty = self.difficulty_levels[current_idx - 1]
            print(f"正确率 {accuracy:.0%}，难度降低为：{self.current_difficulty}")
        else:
            print(f"正确率 {accuracy:.0%}，难度保持：{self.current_difficulty}")
        
        return self.current_difficulty
    
    def get_stats(self):
        """获取学习统计"""
        total = len(self.history)
        correct = sum(1 for h in self.history if h['is_correct'])
        accuracy = correct / total if total > 0 else 0
        
        return {
            '总题数': total,
            '正确数': correct,
            '正确率': f"{accuracy:.1%}",
            '当前难度': self.current_difficulty
        }


# 测试
if __name__ == "__main__":
    scorer = QuizScorer()
    
    # 模拟答题
    print("模拟答题...")
    for i in range(10):
        # 假设前几题都答对，后面答错
        is_correct = i < 7  # 前7题对，后3题错
        scorer.submit_answer(f"题目{i+1}", "答案", is_correct)
        
        # 每5题调整一次难度
        if (i + 1) % 5 == 0:
            scorer.adjust_difficulty()
    
    print("\n学习统计：")
    stats = scorer.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")