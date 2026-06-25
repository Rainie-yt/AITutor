import numpy as np
from collections import Counter

class KNN:
    """
    K-近邻分类算法
    思路：找最近的K个邻居，投票决定类别
    """
    
    def __init__(self, k=5):
        self.k = k
        self.X_train = None
        self.y_train = None
    
    def fit(self, X, y):
        """
        训练：KNN 其实就是把训练数据存起来
        因为它是"惰性学习"，预测时才计算
        """
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        """预测一批数据的类别"""
        predictions = [self._predict_single(x) for x in X]
        return np.array(predictions)
    
    def _predict_single(self, x):
        """预测单个样本"""
        # 计算到所有训练样本的距离
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        
        # 找最近的 k 个邻居
        k_indices = np.argsort(distances)[:self.k]
        k_labels = [self.y_train[i] for i in k_indices]
        
        # 投票：出现次数最多的类别就是预测结果
        most_common = Counter(k_labels).most_common(1)
        return most_common[0][0]
    
    def get_explanation(self):
        return """
        KNN 算法原理（K-近邻）：
        1. 计算新样本到所有训练样本的距离
        2. 找出距离最近的 K 个邻居
        3. 这 K 个邻居中，哪个类别最多，新样本就属于哪类
        
        关键特点：
        - 惰性学习：训练时什么都不做，预测时才计算
        - 没有显式的"模型参数"
        - K 值很重要：太小容易过拟合，太大容易欠拟合
        """


# 测试代码
if __name__ == "__main__":
    # 简单测试：造点数据
    np.random.seed(42)
    X_train = np.array([
        [1, 2], [2, 3], [3, 1], [1, 3],  # 类别0
        [7, 8], [8, 7], [9, 9], [7, 7],  # 类别1
    ])
    y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    
    knn = KNN(k=3)
    knn.fit(X_train, y_train)
    
    # 预测两个新点
    X_test = np.array([[2, 2], [8, 8]])
    predictions = knn.predict(X_test)
    
    print("预测结果：", predictions)
    print("第一个点应该是类别0，第二个点应该是类别1")
    