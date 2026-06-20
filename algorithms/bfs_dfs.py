from collections import deque

class GraphSearch:
    """
    图的广度优先搜索(BFS)和深度优先搜索(DFS)
    用邻接表表示图
    """
    
    def __init__(self, graph=None):
        """
        graph: 字典形式的邻接表
        例如: {'A': ['B', 'C'], 'B': ['A', 'D'], ...}
        """
        self.graph = graph if graph else {}
    
    def add_edge(self, u, v):
        """添加一条边（无向图）"""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def bfs(self, start):
        """
        广度优先搜索：一层一层往外扩散
        用队列实现
        返回遍历顺序
        """
        visited = set()
        queue = deque([start])
        visited.add(start)
        order = []
        
        while queue:
            node = queue.popleft()  # 队首出队
            order.append(node)
            
            # 把所有未访问的邻居入队
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return order
    
    def dfs_recursive(self, start, visited=None, order=None):
        """
        深度优先搜索（递归版）
        一条路走到黑，走不通再回溯
        """
        if visited is None:
            visited = set()
        if order is None:
            order = []
        
        visited.add(start)
        order.append(start)
        
        for neighbor in self.graph[start]:
            if neighbor not in visited:
                self.dfs_recursive(neighbor, visited, order)
        
        return order
    
    def dfs_iterative(self, start):
        """
        深度优先搜索（迭代版，用栈）
        """
        visited = set()
        stack = [start]
        order = []
        
        while stack:
            node = stack.pop()  # 栈顶弹出
            if node not in visited:
                visited.add(node)
                order.append(node)
                # 注意：栈是后进先出，所以要倒序入栈
                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return order
    
    def get_explanation(self):
        return """
        BFS（广度优先搜索）：
        - 像水波纹一样，从起点一层一层扩散
        - 用队列实现（先进先出）
        - 特点：能找到最短路径
        
        DFS（深度优先搜索）：
        - 一条路走到黑，走不通再回溯
        - 用栈实现（或递归）
        - 特点：内存占用小，适合找所有路径
        
        对比：
        - BFS 找最短路径，DFS 找所有路径/拓扑排序
        - BFS 空间复杂度高，DFS 可能栈溢出
        """


# 测试代码
if __name__ == "__main__":
    # 构建一个简单的图
    g = GraphSearch()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    
    print("图结构：", g.graph)
    print("\nBFS 遍历：", g.bfs('A'))
    print("DFS 递归遍历：", g.dfs_recursive('A'))
    print("DFS 迭代遍历：", g.dfs_iterative('A'))
    