from flask import Flask, request, jsonify
from code_analysis import CodeAnalyzer
from flask import Flask
from flask_cors import CORS
from run_code import execute_code
from code_generator import generate_code
from comment import generate_comment_for_code
import random

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], methods=["POST", "GET"], supports_credentials=True)


@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json.get('code')
    random_id = random.randint(1000, 9999)
    filename = f"flowchart{random_id}"
    analyzer = CodeAnalyzer(code)
    analyzer.generate_flowchart(filename)
    
    relative_path = f"/images/{filename}.png"
    return jsonify({"path": relative_path})

@app.route("/run", methods=["POST"])
def run_code():
    data = request.json
    language = data.get("language")
    code = data.get("code")
    return execute_code(language,code)

@app.route("/generate",methods=["POST"])
def generate():
    data=request.json.get('prompt')
    response = generate_code(data)
    return jsonify({"response": response})

@app.route("/explain", methods=["POST"])
def explain():
    data=request.json.get('code')
    response= generate_code("Explain this code in detail "+ data)
    return jsonify({"response": response})

@app.route("/comment", methods=["POST"])
def comment():
    data = request.json.get('code')
    response = generate_comment_for_code(data)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)