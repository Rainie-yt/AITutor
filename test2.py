from flask import Flask 
app = Flask(__name__) 
@app.route('/') 
def hello(): 
    return "SUCCESS!" 
print("SERVER STARTING...") 
app.run(port=5000) 
