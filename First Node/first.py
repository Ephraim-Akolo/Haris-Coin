from hashlib import sha256
import requests
import json
import rsa
from datetime import datetime


class FirstNode:
    def __init__(self, mother:str, mining_deposit_account) -> None:
        self.mother = mother
        self.public_key = mining_deposit_account
        self.getChain('all')
    
    def blockCount(self) -> int:
        '''
        counts the number of blocks in server pool
        '''
        r = requests.get(self.mother + 'blockcount')
        assert r.status_code == 200
        return r.json()['blocks']
    
    def getBlock(self, index) -> dict:
        '''
        gets block of unverified data from the server pool
        '''
        r = requests.get(self.mother + f'getblock/{index}')
        assert r.status_code == 200
        return r.json()
    
    def getChain(self, position:str) -> None:
        '''
        get the blockchain (ledger)
        
        position: str
            can range from -1 to infinity
            -1: all the transaction blocks(complete history/ledger)
            0-infinity: the specific block
        '''
        r = requests.get(self.mother + f'getchain/{position}')
        assert r.status_code == 200
        self.CHAIN = r.json()

    
    def getDifficulty(self) -> str:
        '''
        get difficulty from server
        '''
        r = requests.get(self.mother + 'getdifficulty')
        assert r.status_code == 200
        return str(r.json()['difficulty'])
    
    def getCurrentHash(self) -> str:
        '''
        get last uploaded block's hash
        '''
        r = requests.get(self.mother + 'getcurrenthash')
        assert r.status_code == 200
        return r.json()['hash']

    def getHash(self, block) -> str:
        '''
        Proof of work function
        '''
        order = ('time', 'difficulty', 'verifier', 'token', 'previousHash')
        nonce = 0
        data = ''
        for item in order:
            data += block[item]
        while True:
            hash = sha256((data + str(nonce)).encode('utf-8')).hexdigest()
            if int(hash, 16) < (16**(64 - int(block['difficulty']))):
                return (hash, nonce)
            nonce += 1


            
    
    def checkBalace(self, public_key) -> float:
        '''
        returns the balanced amount of coin from the blockchain
        '''
        negatives = 0
        positives = 0
        r = requests.get(self.mother + 'motherkey', json={'key': public_key})
        assert r.status_code == 200
        if r.json()['ismother'] == True:
            for blockNum in range(self.CHAIN['size']):
                for transNum in range(self.CHAIN[str(blockNum)]['size']):
                    transaction = self.CHAIN[str(blockNum)][str(transNum)]
                    if public_key == transaction['sender']:
                        negatives += float(transaction['amount'])
                        negatives += float(self.CHAIN[str(blockNum)]['token'])
                    elif public_key == transaction['receiver']:
                        positives += float(transaction['amount'])
                    positives += (0.25 * float(self.CHAIN[str(blockNum)]['token']))
        else:
            for blockNum in range(self.CHAIN['size']):
                for transNum in range(self.CHAIN[str(blockNum)]['size']):
                    transaction = self.CHAIN[str(blockNum)][str(transNum)]
                    if public_key == transaction['sender']:
                        negatives += float(transaction['amount'])
                        negatives += float(transaction['token'])
                    elif public_key == transaction['receiver']:
                        positives += float(transaction['amount'])
                    if public_key == self.CHAIN[str(blockNum)]['verifier']:
                        positives += (0.75 * float(self.CHAIN[str(blockNum)]['token']))
        return (positives - negatives)
        
    def getTokenAmount(self):
        '''
        get the token amount from the server
        '''
        r = requests.get(self.mother + 'gettoken')
        assert r.status_code == 200
        return r.json()['token']
    
    def signatureVerified(self, data) -> bool:
        '''
        function that verifies the sender signature.
        '''
        order = ('id', 'sender', 'receiver', 'amount')
        sender = rsa.PrivateKey.load_pkcs1(data['sender'].encode('utf-8'), 'PEM')
        appendedData = sha256()
        for value in order:
            appendedData.update(data[value].encode('utf-8'))
        hash = rsa.decrypt(data['signature'].encode('ISO-8859-1'), sender)
        assert type(hash.decode('utf-8')) == type(appendedData.hexdigest())
        if hash.decode('utf-8') == appendedData.hexdigest():
            return True
        else:
            return False
        

    def blocksVerified(self, block) -> dict:
        '''
        verifies the sender balance and the signature.
        '''
        vblock = {'size': 0}
        n = 0
        for num in range(block['size']):
            transaction = block[str(num)]
            sender = transaction['sender']
            balance = self.checkBalace(sender)
            token = self.getTokenAmount()
            if (balance > (int(transaction['amount']) + float(token))) and self.signatureVerified(transaction):
                vblock['size'] += 1
                vblock[str(n)] = transaction
                n += 1
        return vblock


    def summitMinnedBlock(self, block, index):
        '''
        submits mined and verified block.
        '''
        r = requests.get(self.mother + f'summitminnedblock/{index}', json=block)
        assert r.status_code == 200
        return r.json()
    
    def mineBlock(self, index):
        '''
        mines an unverified block from the server transaction pool.
        '''
        block = self.getBlock(index)
        block = self.blocksVerified(block)
        block['time'] = datetime.now().strftime("%I:%M%p %B %d %Y")
        block['difficulty'] = self.getDifficulty()
        block['verifier'] = self.public_key.decode('utf-8')
        block['token'] = self.getTokenAmount()
        block['previousHash'] = self.getCurrentHash()
        (block['hash'], nonce) = self.getHash(block)
        block['nonce'] = str(nonce)
        r = self.summitMinnedBlock(block, index)
        print(r)
