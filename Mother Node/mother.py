from flask import Flask, request, jsonify


app = Flask(__name__)
@app.route('/<dest>', methods=['GET', 'POST'])
def index(dest):
    content = request.json
    print(type(content))
    return jsonify({'message': dest})