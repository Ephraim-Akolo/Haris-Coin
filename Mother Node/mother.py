from flask import Flask, request, jsonify
from hashlib import sha256

app = Flask(__name__)

# data base in reality will be a relational Database
POOL = []
blockSize = 99
difficulty = 5
token = 0.2
startNewBlock = False
public_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEqQIBAAKCAQEA5Rlbzb4+t8Bg+4UByA5ZOoc7RiSItriA7fUPtaPfiVy/6yr2\n69w8SlqUh5nQBo9aDPXZJpRS1DaD87Ob5ibremq7BuVaj8/qi3YA9M5Q7JDuiuNY\n7pcfWBfTsaJ21Lzi2Bd8CpZ7n5l1oE/oq/rEaczpVr+hrLBjl2Hb5BG6SajTeePW\nloe6xAVqz1qrNYrsA8Wv4qj3jkTuV1r94PNwrqE/Gq+ohXCP05acWwZPE1lZkjoo\nqEMBVYn0HcwpwOqDNw9WUvORxDmVU6VUO10oRkyTMI3/kbIdWDCrqxfogduMZDR+\n+Tlsc79wVREJqtA9Y4F1dRRQmacwQ37VpjIHjQIDAQABAoIBAF6BvoA6Ga89egRn\n0ttPJ/nf7VC7I3aU2ALRlABvMHh+vWDqoV+cw3Y8tYbWqZz7J7+u7zxd9Wk7b+Vp\nU0d3CK7ANpTaqignMe8D59MVBQcBppW+wWHzD2gMtDRT+8c4gC96SJ4pg6fL610N\necLwOHQYpq01ciFFxfaB8VDLeLWEYmEtMenkvZvY2f8Ktg9qGLvhwoml9tI1nFx8\nsJ7CKQ07h1Yxy8UTiYHXFY/ZHy8U8rTOeax0pmkOH6OC0ao4SibG4NFBe1XMlfpw\n1kuYRc9rLg6M6YM8ToOroqqvOtHURLQyiYvnMVFBAIUCOJLNc+5bhEHG3ox1Q2Gs\n6ofmAUECgYkA/sveTtsChNnBI3CurxZNePbcV25+hybStOWjOhX/cmW8UJAHZpJ/\nEF9mwz0uOfL1Q4efSnCFo+72R4jvFsYDScbNc/t7kyDr9YBfFEn9LaAXGOcy9khL\nwKpxrb501jRtJDe/U8Fccro2mqrRyMZw0WwojV28ub7mFmbBAizNW+vgsvNUQcIC\nvQJ5AOYuafB2jwvkTLiT7BghU6HF0iwFaoxaOvK5dxK03PaRPdAZh6T5pBnasPoY\naGX26x3s/WesuGETYLipnW1qvb772QNEYxWCzd++FjyxX/QwNT1kUB+e9YZPRwpW\nSULNMV+jzT4JsO67zLdxXb+6vK/m5IFtocFNEQKBiQD19Jg5aKKK2aTd8CU/8HiC\nn1HduFS9ZBWb99xT8u4uYNSitBXgxuOPS3hoWUOpPsXRFTcH5Yyrzb3BGgcp5aVA\n735eSlFkmjAMQYoGjNGv3EzPhkakhO9TIXUw8ZvZNqxwfLvdPtdeDDEvpltxw1Ue\nY5jVtbm7V/LFhxUjY1otNIooVEluXLjFAnh7OvIAiJiAl1Lzpk3JhV4Ox6eDZcrr\nJQtWEzDKVQXPA2cCWAikq/nM1aXV3udVX2H0fYIU1QVJA2TOuA/OGk1HR/GgrCYX\nyBWL6WpiR9vFEWIPYfr7UtDDfQHdaOCD4PLD7x/cTLfqt6QbuZelI8YMriI7oIPu\nxuECgYhhAwclUYxwVpZxqdL2KvxVP9yHiI7PMPm4HzKpWzKr6ufPSaI+nbMWPnhv\nX+1YxgKj/U/uSNsyWvWaCMZ8oySGrn1qtmeoeE3SqJGg+GzTzCHaZC3HVOOlV2HL\nJIn0s/g+5E/8SlPtSCQLc7xr420Rcf6YAOb+SNWQ6Ma9Vq7+LbNlNFbzX0kI\n-----END RSA PRIVATE KEY-----\n"
firstTransaction = {
    'id': '#',
    'sender': '#',
    'receiver': "-----BEGIN RSA PRIVATE KEY-----\nMIIEqQIBAAKCAQEA5Rlbzb4+t8Bg+4UByA5ZOoc7RiSItriA7fUPtaPfiVy/6yr2\n69w8SlqUh5nQBo9aDPXZJpRS1DaD87Ob5ibremq7BuVaj8/qi3YA9M5Q7JDuiuNY\n7pcfWBfTsaJ21Lzi2Bd8CpZ7n5l1oE/oq/rEaczpVr+hrLBjl2Hb5BG6SajTeePW\nloe6xAVqz1qrNYrsA8Wv4qj3jkTuV1r94PNwrqE/Gq+ohXCP05acWwZPE1lZkjoo\nqEMBVYn0HcwpwOqDNw9WUvORxDmVU6VUO10oRkyTMI3/kbIdWDCrqxfogduMZDR+\n+Tlsc79wVREJqtA9Y4F1dRRQmacwQ37VpjIHjQIDAQABAoIBAF6BvoA6Ga89egRn\n0ttPJ/nf7VC7I3aU2ALRlABvMHh+vWDqoV+cw3Y8tYbWqZz7J7+u7zxd9Wk7b+Vp\nU0d3CK7ANpTaqignMe8D59MVBQcBppW+wWHzD2gMtDRT+8c4gC96SJ4pg6fL610N\necLwOHQYpq01ciFFxfaB8VDLeLWEYmEtMenkvZvY2f8Ktg9qGLvhwoml9tI1nFx8\nsJ7CKQ07h1Yxy8UTiYHXFY/ZHy8U8rTOeax0pmkOH6OC0ao4SibG4NFBe1XMlfpw\n1kuYRc9rLg6M6YM8ToOroqqvOtHURLQyiYvnMVFBAIUCOJLNc+5bhEHG3ox1Q2Gs\n6ofmAUECgYkA/sveTtsChNnBI3CurxZNePbcV25+hybStOWjOhX/cmW8UJAHZpJ/\nEF9mwz0uOfL1Q4efSnCFo+72R4jvFsYDScbNc/t7kyDr9YBfFEn9LaAXGOcy9khL\nwKpxrb501jRtJDe/U8Fccro2mqrRyMZw0WwojV28ub7mFmbBAizNW+vgsvNUQcIC\nvQJ5AOYuafB2jwvkTLiT7BghU6HF0iwFaoxaOvK5dxK03PaRPdAZh6T5pBnasPoY\naGX26x3s/WesuGETYLipnW1qvb772QNEYxWCzd++FjyxX/QwNT1kUB+e9YZPRwpW\nSULNMV+jzT4JsO67zLdxXb+6vK/m5IFtocFNEQKBiQD19Jg5aKKK2aTd8CU/8HiC\nn1HduFS9ZBWb99xT8u4uYNSitBXgxuOPS3hoWUOpPsXRFTcH5Yyrzb3BGgcp5aVA\n735eSlFkmjAMQYoGjNGv3EzPhkakhO9TIXUw8ZvZNqxwfLvdPtdeDDEvpltxw1Ue\nY5jVtbm7V/LFhxUjY1otNIooVEluXLjFAnh7OvIAiJiAl1Lzpk3JhV4Ox6eDZcrr\nJQtWEzDKVQXPA2cCWAikq/nM1aXV3udVX2H0fYIU1QVJA2TOuA/OGk1HR/GgrCYX\nyBWL6WpiR9vFEWIPYfr7UtDDfQHdaOCD4PLD7x/cTLfqt6QbuZelI8YMriI7oIPu\nxuECgYhhAwclUYxwVpZxqdL2KvxVP9yHiI7PMPm4HzKpWzKr6ufPSaI+nbMWPnhv\nX+1YxgKj/U/uSNsyWvWaCMZ8oySGrn1qtmeoeE3SqJGg+GzTzCHaZC3HVOOlV2HL\nJIn0s/g+5E/8SlPtSCQLc7xr420Rcf6YAOb+SNWQ6Ma9Vq7+LbNlNFbzX0kI\n-----END RSA PRIVATE KEY-----\n",
    'amount': '1000000000',
    'signature': '#'
}
firstBlock = {
    'size': 1,
    '0': firstTransaction,
    'time': '#',
    'difficulty': '0',
    'verifier': '',
    'token': '0',
    'previousHash': '#',
    'nonce': '1',
    'hash': '26fb897befac9d2cf7598d6f7636ca7d79a1d1962c7b3d7b2abf0354ce136742'
}
CHAIN = {
    'size': 1,
    '0': firstBlock
    }

def addToCurrentBlock(content) -> None:
    blocks = len(POOL)
    global startNewBlock
    if blocks == 0 or startNewBlock:
        POOL.append({'size': 1,'0': content})
        startNewBlock = False
        return
    elif POOL[blocks-1]['size'] >= blockSize:
        POOL.append({'size': 1,'0': content})
        return
    ## check if transaction is aready in blocks(by check if the signature and id are thesame) and exit if true

    ## end of check
    size = POOL[blocks-1]['size']
    POOL[blocks-1]['size'] += 1
    POOL[blocks-1][str(size)] = content


@app.route('/')
def index():
    return 'OK'

@app.route('/pool', methods=['GET'])
def pool():
    content = request.json
    # we assume that what ever is being sent to the pool is genuine 
    addToCurrentBlock(content)
    print(content, "block received successfuly!", sep='\n')
    return jsonify({'in_pool': True})

@app.route('/getblock/<index>', methods=['GET'])
def getBlock(index):
    if int(index) == len(POOL) - 1: # if you are requesting for the current updating block
        if len(POOL) <= 1:
            global startNewBlock
            startNewBlock = True
        else:
            return jsonify({'error': 'index currently updating!'})
    return jsonify(POOL[int(index)])

@app.route('/blockcount', methods=['GET'])
def blockCount():
    return jsonify({'blocks': len(POOL)})

@app.route('/getchain/<position>', methods=['GET'])
def getChain(position):
    if position == '-1' or position == 'all':
        return jsonify(CHAIN)
    elif int(position) > -1 and int(position) < CHAIN['size']:
        return jsonify(CHAIN[position])

@app.route('/getdifficulty', methods=['GET'])
def getDifficulty():
    return jsonify({'difficulty': difficulty})

@app.route('/gettoken', methods = ['GET'])
def getToken():
    return jsonify({'token': str(token)})

@app.route('/motherkey', methods = ['GET'])
def ismother():
    key = request.json['key']
    if key == public_key:
        return jsonify({'ismother': True}) 
    else:
        return jsonify({'ismother': False})

@app.route('/getcurrenthash', methods = ['GET'])
def getCurrentHash():
    recentIndex = CHAIN['size'] - 1
    hash = CHAIN[str(recentIndex)]['hash']
    return jsonify({'hash': hash})

@app.route('/summitminnedblock/<index>', methods = ['GET'])
def summitMinnedBlock(index):
    block = request.json
    # check mined block to confirm prove of work
    order = ('time', 'difficulty', 'verifier', 'token', 'previousHash', 'nonce')
    data = ''
    
    for item in order:
        data += block[item]
    hash = sha256(data.encode('utf-8')).hexdigest()
    print(hash, 'and', block['hash'])
    if hash != block['hash']:
        return jsonify({'submit_status': False, 'Error': 'invalid hash'})
    # check if block is empyty
    try:
        block['0']
    except:
        POOL.pop(int(index))
        return jsonify({'submit_status': False, 'Error': 'empty block'})
    # confirm block is in pool
    size = POOL[int(index)]['size']
    _block_ = POOL[int(index)]
    for i in range(size):
        if block['0']['sender'] == _block_[str(i)]['sender'] and block['0']['signature'] == _block_[str(i)]['signature']:
            break
    else:
        return jsonify({'submit_status': False, 'Error': 'invalid block'})
    # add block to chain
    CHAIN[str(CHAIN['size'])] = block
    CHAIN['size'] += 1
    # remove from pool
    POOL.pop(int(index))
    return jsonify({'submit_status': True, 'Error': 'None'})
    
