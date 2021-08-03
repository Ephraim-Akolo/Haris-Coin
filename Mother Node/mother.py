from flask import Flask, request, jsonify

app = Flask(__name__)

# data base in reality will be a relational Database
POOL = []
blockSize = 99
startNewBlock = False
firstBlock = {
    'id': '#',
    'sender': '#',
    'receiver': "-----BEGIN RSA PRIVATE KEY-----\nMIIEqQIBAAKCAQEA5Rlbzb4+t8Bg+4UByA5ZOoc7RiSItriA7fUPtaPfiVy/6yr2\n69w8SlqUh5nQBo9aDPXZJpRS1DaD87Ob5ibremq7BuVaj8/qi3YA9M5Q7JDuiuNY\n7pcfWBfTsaJ21Lzi2Bd8CpZ7n5l1oE/oq/rEaczpVr+hrLBjl2Hb5BG6SajTeePW\nloe6xAVqz1qrNYrsA8Wv4qj3jkTuV1r94PNwrqE/Gq+ohXCP05acWwZPE1lZkjoo\nqEMBVYn0HcwpwOqDNw9WUvORxDmVU6VUO10oRkyTMI3/kbIdWDCrqxfogduMZDR+\n+Tlsc79wVREJqtA9Y4F1dRRQmacwQ37VpjIHjQIDAQABAoIBAF6BvoA6Ga89egRn\n0ttPJ/nf7VC7I3aU2ALRlABvMHh+vWDqoV+cw3Y8tYbWqZz7J7+u7zxd9Wk7b+Vp\nU0d3CK7ANpTaqignMe8D59MVBQcBppW+wWHzD2gMtDRT+8c4gC96SJ4pg6fL610N\necLwOHQYpq01ciFFxfaB8VDLeLWEYmEtMenkvZvY2f8Ktg9qGLvhwoml9tI1nFx8\nsJ7CKQ07h1Yxy8UTiYHXFY/ZHy8U8rTOeax0pmkOH6OC0ao4SibG4NFBe1XMlfpw\n1kuYRc9rLg6M6YM8ToOroqqvOtHURLQyiYvnMVFBAIUCOJLNc+5bhEHG3ox1Q2Gs\n6ofmAUECgYkA/sveTtsChNnBI3CurxZNePbcV25+hybStOWjOhX/cmW8UJAHZpJ/\nEF9mwz0uOfL1Q4efSnCFo+72R4jvFsYDScbNc/t7kyDr9YBfFEn9LaAXGOcy9khL\nwKpxrb501jRtJDe/U8Fccro2mqrRyMZw0WwojV28ub7mFmbBAizNW+vgsvNUQcIC\nvQJ5AOYuafB2jwvkTLiT7BghU6HF0iwFaoxaOvK5dxK03PaRPdAZh6T5pBnasPoY\naGX26x3s/WesuGETYLipnW1qvb772QNEYxWCzd++FjyxX/QwNT1kUB+e9YZPRwpW\nSULNMV+jzT4JsO67zLdxXb+6vK/m5IFtocFNEQKBiQD19Jg5aKKK2aTd8CU/8HiC\nn1HduFS9ZBWb99xT8u4uYNSitBXgxuOPS3hoWUOpPsXRFTcH5Yyrzb3BGgcp5aVA\n735eSlFkmjAMQYoGjNGv3EzPhkakhO9TIXUw8ZvZNqxwfLvdPtdeDDEvpltxw1Ue\nY5jVtbm7V/LFhxUjY1otNIooVEluXLjFAnh7OvIAiJiAl1Lzpk3JhV4Ox6eDZcrr\nJQtWEzDKVQXPA2cCWAikq/nM1aXV3udVX2H0fYIU1QVJA2TOuA/OGk1HR/GgrCYX\nyBWL6WpiR9vFEWIPYfr7UtDDfQHdaOCD4PLD7x/cTLfqt6QbuZelI8YMriI7oIPu\nxuECgYhhAwclUYxwVpZxqdL2KvxVP9yHiI7PMPm4HzKpWzKr6ufPSaI+nbMWPnhv\nX+1YxgKj/U/uSNsyWvWaCMZ8oySGrn1qtmeoeE3SqJGg+GzTzCHaZC3HVOOlV2HL\nJIn0s/g+5E/8SlPtSCQLc7xr420Rcf6YAOb+SNWQ6Ma9Vq7+LbNlNFbzX0kI\n-----END RSA PRIVATE KEY-----\n",
    'amount': '1000000000',
    'token': '#',
    'signature': '#',
    'time': '#',
    'previousHash': '#',
    'difficulty': '0',
    'nounce': '1',
    'hash': '2948cf22c54dca70b3b9da3d5a49e0453304d03ca3f253be5d9f28f3e6c10232'
}
CHAIN = {
    'size': 1,
    '0': firstBlock
    }

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


