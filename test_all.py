import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """测试健康检查"""
    print("="*60)
    print("测试1：健康检查")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/api/health")
        print(f"状态码：{r.status_code}")
        print(f"返回：{json.dumps(r.json(), ensure_ascii=False, indent=2)}")
        print("✅ 健康检查通过")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败：{e}")
        return False

def test_knowledge():
    """测试知识库列表"""
    print("\n" + "="*60)
    print("测试2：知识库列表")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/api/knowledge")
        print(f"状态码：{r.status_code}")
        data = r.json()
        print(f"知识库数量：{len(data['knowledge'])}")
        for item in data['knowledge']:
            print(f"  - {item['name']}")
        print("✅ 知识库接口通过")
        return True
    except Exception as e:
        print(f"❌ 知识库接口失败：{e}")
        return False

def test_chat():
    """测试聊天接口"""
    print("\n" + "="*60)
    print("测试3：聊天接口")
    print("="*60)
    try:
        # 测试概念问题
        r = requests.post(f"{BASE_URL}/api/chat", 
                         json={'question': '什么是K-means？', 'user_id': 'test'})
        print(f"状态码：{r.status_code}")
        data = r.json()
        print(f"使用Agent：{data['agent']}")
        print(f"回答前100字：{data['answer'][:100]}...")
        print(f"对话轮数：{data['history_count']}")
        print("✅ 聊天接口通过")
        return True
    except Exception as e:
        print(f"❌ 聊天接口失败：{e}")
        return False

def test_quiz():
    """测试测验接口"""
    print("\n" + "="*60)
    print("测试4：测验系统")
    print("="*60)
    try:
        # 抽题
        print("4.1 抽取题目...")
        r = requests.post(f"{BASE_URL}/api/quiz/get", 
                         json={'concept': 'kmeans'})
        print(f"状态码：{r.status_code}")
        quiz_data = r.json()
        print(f"题目：{quiz_data['data']['question']}")
        print(f"选项：{quiz_data['data']['options']}")
        
        # 提交答案
        print("\n4.2 提交答案...")
        r = requests.post(f"{BASE_URL}/api/quiz/submit", 
                         json={'user_answer': '测试答案'})
        print(f"状态码：{r.status_code}")
        result = r.json()
        print(f"是否正确：{result['data']['is_correct']}")
        print(f"正确答案：{result['data']['correct_answer']}")
        
        # 错题本
        print("\n4.3 查看错题本...")
        r = requests.get(f"{BASE_URL}/api/quiz/error")
        print(f"状态码：{r.status_code}")
        error_data = r.json()
        print(f"错题数量：{error_data['count']}")
        
        print("✅ 测验系统通过")
        return True
    except Exception as e:
        print(f"❌ 测验系统失败：{e}")
        return False

def test_knowledge_graph():
    """测试知识图谱"""
    print("\n" + "="*60)
    print("测试5：知识图谱")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/api/knowledge_graph")
        print(f"状态码：{r.status_code}")
        data = r.json()
        print(f"返回数据量：{len(str(data))} 字符")
        print("✅ 知识图谱接口通过")
        return True
    except Exception as e:
        print(f"❌ 知识图谱接口失败：{e}")
        return False

def test_clear_history():
    """测试清空历史"""
    print("\n" + "="*60)
    print("测试6：清空对话历史")
    print("="*60)
    try:
        r = requests.post(f"{BASE_URL}/api/chat/clear", 
                         json={'user_id': 'test'})
        print(f"状态码：{r.status_code}")
        print(f"返回：{r.json()['message']}")
        print("✅ 清空历史通过")
        return True
    except Exception as e:
        print(f"❌ 清空历史失败：{e}")
        return False

if __name__ == '__main__':
    print("\n" + "🚀"*20)
    print("  AI导学系统 - 全面测试")
    print("🚀"*20 + "\n")
    
    results = []
    results.append(("健康检查", test_health()))
    results.append(("知识库列表", test_knowledge()))
    results.append(("聊天接口", test_chat()))
    results.append(("测验系统", test_quiz()))
    results.append(("知识图谱", test_knowledge_graph()))
    results.append(("清空历史", test_clear_history()))
    
    print("\n" + "="*60)
    print("  📊 测试结果汇总")
    print("="*60)
    
    passed = 0
    failed = 0
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}：{status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-"*60)
    print(f"  总计：{len(results)} 项，通过 {passed} 项，失败 {failed} 项")
    print("="*60)
    
    if failed == 0:
        print("\n🎉🎉🎉 所有测试全部通过！系统运行正常！")
    else:
        print(f"\n⚠️  有 {failed} 项测试失败，请检查")