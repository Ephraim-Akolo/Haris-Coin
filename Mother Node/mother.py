from flask import Flask, request, jsonify


app = Flask(__name__)

# data base in reality will be a relational Database
POOL = []
CHAIN = {}
blockSize = 99
startNewBlock = False

def addToCurrentBlock(content) -> None:
    blocks = len(POOL)
    global startNewBlock
    if blocks == 0 or startNewBlock:
        POOL.append({'size': 1,'1': content})
        startNewBlock = False
        return
    elif POOL[blocks-1]['size'] > blockSize:
        POOL.append({'size': 1,'1': content})
        return
    ## check if block is aready in pool and exit if true

    ## end of check
    POOL[blocks-1]['size'] += 1
    size = POOL[blocks-1]['size']
    POOL[blocks-1][str(size)] = content
    print(POOL)


@app.route('/')
def index():
    return 'OK'

@app.route('/pool', methods=['GET', 'POST'])
def pool():
    content = request.json
    # we assume that what ever is being sent to the pool is genuine 
    addToCurrentBlock(content)
    print(content, "block received successfuly!", sep='\n')
    return jsonify({'in_pool': True})

@app.route('/getblock/<index>', methods=['GET', 'POST'])
def getBlock(index):
    if int(index) == len(POOL) - 1: # if you are requesting for the current updating block
        if len(POOL) <= 1:
            global startNewBlock
            startNewBlock = True
        else:
            return jsonify({'error': 'index currently updating!'})
    return jsonify(POOL[int(index)])

@app.route('/blockcount', methods=['GET', 'POST'])
def blockCount():
    return jsonify({'blocks': len(POOL)})


