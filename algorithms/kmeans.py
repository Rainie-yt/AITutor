import numpy as np

class KMeans:
    """
    K-means 聚类算法的简单实现
    用于教学演示，帮助理解聚类原理
    """
    
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-4):
        """
        参数说明：
        - n_clusters: 聚类数量（K值）
        - max_iter: 最大迭代次数
        - tol: 收敛阈值，中心点变化小于这个值就停止
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = None  # 中心点
        self.labels = None     # 每个样本的类别
    
    def fit(self, X):
        """
        训练模型：找到最优的聚类中心
        X: 形状为 (n_samples, n_features) 的数据
        """
        n_samples, n_features = X.shape
        
        # 步骤1：随机初始化中心点（从数据中随机选K个）
        random_idx = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[random_idx]
        
        for i in range(self.max_iter):
            # 步骤2：分配样本到最近的中心点
            self.labels = self._assign_clusters(X)
            
            # 步骤3：更新中心点（计算每个簇的均值）
            old_centroids = self.centroids.copy()
            for k in range(self.n_clusters):
                cluster_samples = X[self.labels == k]
                if len(cluster_samples) > 0:
                    self.centroids[k] = np.mean(cluster_samples, axis=0)
            
            # 步骤4：检查是否收敛
            diff = np.sum(np.abs(self.centroids - old_centroids))
            if diff < self.tol:
                print(f"K-means 在第 {i+1} 次迭代后收敛")
                break
    
    def _assign_clusters(self, X):
        """把每个样本分配到最近的中心点"""
        distances = np.zeros((len(X), self.n_clusters))
        for k in range(self.n_clusters):
            # 计算每个样本到第k个中心点的欧氏距离
            distances[:, k] = np.sqrt(np.sum((X - self.centroids[k]) ** 2, axis=1))
        # 返回距离最小的那个簇的索引
        return np.argmin(distances, axis=1)
    
    def predict(self, X):
        """预测新数据属于哪个簇"""
        return self._assign_clusters(X)
    
    def get_explanation(self):
        """返回算法原理的文字说明（用于Agent调用）"""
        return """
        K-means 算法原理：
        1. 随机选择 K 个点作为初始聚类中心
        2. 将每个样本分配到距离最近的中心点
        3. 重新计算每个簇的中心点（均值）
        4. 重复步骤2-3，直到中心点不再明显变化
        
        为什么会收敛？
        - 每次迭代都会让"样本到中心的距离总和"变小或不变
        - 这个总和有下界（不可能无限小）
        - 所以一定会收敛到局部最优
        """


# 测试代码
if __name__ == "__main__":
    # 生成测试数据：3个簇
    np.random.seed(42)
    X1 = np.random.randn(50, 2) + np.array([0, 0])      # 簇1：中心在(0,0)
    X2 = np.random.randn(50, 2) + np.array([5, 5])      # 簇2：中心在(5,5)
    X3 = np.random.randn(50, 2) + np.array([0, 5])      # 簇3：中心在(0,5)
    X = np.vstack([X1, X2, X3])
    
    # 运行 K-means
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)
    
    print("最终中心点：")
    print(kmeans.centroids)
    print("\n前10个样本的类别：")
    print(kmeans.labels[:10])
    