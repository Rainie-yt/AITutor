import numpy as np

class SimpleNeuralNetwork:
    """
    一个最简单的两层神经网络（输入层 + 隐藏层 + 输出层）
    用 numpy 从零实现，帮助理解反向传播
    """
    
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        """
        参数：
        - input_size: 输入特征数量
        - hidden_size: 隐藏层神经元数量
        - output_size: 输出类别数量
        - learning_rate: 学习率
        """
        self.lr = learning_rate
        
        # 初始化权重和偏置
        # W1: 输入层到隐藏层的权重
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        
        # W2: 隐藏层到输出层的权重
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def sigmoid(self, x):
        """Sigmoid 激活函数：把值压缩到 (0,1) 之间"""
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        """Sigmoid 的导数（用于反向传播）"""
        return x * (1 - x)
    
    def forward(self, X):
        """
        前向传播：计算预测值
        返回各层的输出（反向传播要用）
        """
        # 隐藏层
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        
        # 输出层
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        
        return self.a2
    
    def backward(self, X, y, output):
        """
        反向传播：计算梯度，更新权重
        核心是链式法则
        """
        m = X.shape[0]  # 样本数量
        
        # 输出层误差
        dZ2 = output - y  # 误差（简化版，配合 sigmoid + 均方误差）
        dW2 = np.dot(self.a1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        # 隐藏层误差
        dZ1 = np.dot(dZ2, self.W2.T) * self.sigmoid_derivative(self.a1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # 更新权重和偏置（梯度下降）
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
    
    def train(self, X, y, epochs=1000, print_every=100):
        """训练模型"""
        for i in range(epochs):
            # 前向传播
            output = self.forward(X)
            
            # 反向传播
            self.backward(X, y, output)
            
            # 打印损失
            if i % print_every == 0:
                loss = np.mean((y - output) ** 2)
                print(f"第 {i} 轮，损失: {loss:.4f}")
    
    def predict(self, X):
        """预测（返回 0 或 1）"""
        output = self.forward(X)
        return (output > 0.5).astype(int)
    
    def get_explanation(self):
        return """
        神经网络原理（两层为例）：
        
        1. 前向传播（Forward）
           - 输入数据 → 乘以权重 → 加偏置 → 激活函数 → 下一层
           - 公式：a = σ(W·x + b)
           - 目的：计算预测值
        
        2. 反向传播（Backward）
           - 计算预测值和真实值的误差
           - 用链式法则，从后往前算每个权重的梯度
           - 目的：知道每个权重对误差的"贡献"有多大
        
        3. 梯度下降
           - 权重 = 权重 - 学习率 × 梯度
           - 让误差一点点变小
        
        为什么需要激活函数？
        - 如果没有激活函数，多层网络等价于一层
        - 激活函数引入非线性，网络才能学习复杂模式
        """


# 测试代码：用 XOR 问题测试
if __name__ == "__main__":
    # XOR 问题：输入两个数，相同输出0，不同输出1
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    # 创建并训练网络
    nn = SimpleNeuralNetwork(input_size=2, hidden_size=8, output_size=1, learning_rate=1.0)
    nn.train(X, y, epochs=50000, print_every=10000)
    
    # 测试
    predictions = nn.predict(X)
    print("\n预测结果：")
    for i in range(len(X)):
        print(f"输入 {X[i]} → 预测 {predictions[i][0]}，真实 {y[i][0]}")