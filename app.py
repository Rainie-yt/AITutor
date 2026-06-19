from flask import Flask, request, jsonify 
from flask_cors import CORS 
import ollama 
 
app = Flask(__name__) 
CORS(app) 
 
@app.route('/api/health') 
def health(): 
    return jsonify(status="ok", message="后端运行正常！") 
 
@app.route('/api/chat', methods=['POST']) 
def chat(): 
    data = request.get_json() 
    q = data.get('question', '') 
    r = ollama.generate(model='qwen:0.5b', prompt=q) 
    return jsonify(answer=r['response'], agent="默认Agent") 
 
print("AI导学系统启动成功！") 
print("聊天接口：http://localhost:5000/api/chat") 
app.run(port=5000) 
