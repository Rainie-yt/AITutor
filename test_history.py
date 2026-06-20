import requests

print("="*50)
print("测试对话历史功能")
print("="*50)

# 第一轮
print("\n第一轮：什么是K-means？")
r = requests.post('http://localhost:5000/api/chat', 
                  json={'question': '什么是K-means？', 'user_id': 'test'})
print(f"回答：{r.json()['answer'][:100]}...")
print(f"对话轮数：{r.json()['history_count']}")

# 第二轮
print("\n第二轮：它有什么缺点？")
r = requests.post('http://localhost:5000/api/chat', 
                  json={'question': '它有什么缺点？', 'user_id': 'test'})
print(f"回答：{r.json()['answer'][:100]}...")
print(f"对话轮数：{r.json()['history_count']}")

# 清空历史
print("\n清空历史...")
r = requests.post('http://localhost:5000/api/chat/clear', 
                  json={'user_id': 'test'})
print(r.json()['message'])

print("\n✅ 测试完成！")