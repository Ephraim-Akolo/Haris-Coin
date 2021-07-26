from flask import Flask, request, jsonify


app = Flask(__name__)

DATABASE = []

def addToCurrentBlock(content):
    blocks = len(DATABASE)
    if blocks == 0:
        DATABASE.append({'size': 1,'1': content})
        return
    if DATABASE[blocks-1]['size'] > 99:
        DATABASE.append({'size': 1,'1': content})
        return
    DATABASE[blocks-1]['size'] += 1
    size = DATABASE[blocks-1]['size']
    DATABASE[blocks-1][str(size)] = content
    print(DATABASE)


@app.route('/')
def index():
    return 'OK'

@app.route('/pool', methods=['GET', 'POST'])
def pool():
    content = request.json
    addToCurrentBlock(content)
    return jsonify({'in_pool': True})

