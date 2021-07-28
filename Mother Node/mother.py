from flask import Flask, request, jsonify


app = Flask(__name__)

# data base in reality will be a relational database
DATABASE = []

def addToCurrentBlock(content) -> None:
    blocks = len(DATABASE)
    if blocks == 0:
        DATABASE.append({'size': 1,'1': content})
        return
    elif DATABASE[blocks-1]['size'] > 99:
        DATABASE.append({'size': 1,'1': content})
        return
    ## check if block is aready in pool and exit if true

    ## end of check
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
    # we assume that what ever is being sent to the pool is genuine 
    addToCurrentBlock(content)
    return jsonify({'in_pool': True})

@app.route('/getblock/<index>', methods=['GET', 'POST'])
def getBlock(index):
    return jsonify(DATABASE[int(index)])

@app.route('/blockcount', methods=['GET', 'POST'])
def blockCount():
    return jsonify({'blocks': len(DATABASE)})


