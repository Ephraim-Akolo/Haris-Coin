from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return "OK"

@app.route('/pool', methods=['GET', 'POST'])
def pool():
    content = request.json
    print(content)
    return jsonify({'in_pool': True})