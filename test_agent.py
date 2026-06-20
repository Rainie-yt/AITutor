import requests

# 测试1：概念问题
print("测试1：什么是K-means？")
r = requests.post('http://localhost:5000/api/chat', 
                  json={'question': '什么是K-means算法？'})
print(f"Agent: {r.json()['agent']}")
print(r.json()['answer'][:200])
print()

# 测试2：数学问题
print("测试2：K-means为什么会收敛？")
r = requests.post('http://localhost:5000/api/chat', 
                  json={'question': 'K-means为什么会收敛？'})
print(f"Agent: {r.json()['agent']}")
print(r.json()['answer'][:200])
print()

# 测试3：代码问题
print("测试3：给我KNN的Python代码")
r = requests.post('http://localhost:5000/api/chat', 
                  json={'question': '给我KNN的Python代码'})
print(f"Agent: {r.json()['agent']}")
print(r.json()['answer'][:200])