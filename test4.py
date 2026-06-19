from flask import Flask 
app = Flask(__name__) 
@app.route('/') 
def home(): 
    return "SUCCESS!!!" 
print("SERVER IS RUNNING!") 
print("Open: http://localhost:5000") 
app.run(port=5000) 
