import ollama

print("正在调用 Ollama，请稍等...")
response = ollama.chat(
    model='qwen2.5:7b',
    messages=[
        {'role': 'user', 'content': '你好，请用一句话介绍你自己'}
    ]
)

print("回答：")
print(response['message']['content'])
