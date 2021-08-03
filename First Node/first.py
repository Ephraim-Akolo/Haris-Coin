import requests
import json
from datetime import datetime

from rsa import key


class FirstNode:
    def __init__(self, mother:str) -> None:
        # ## Upload Test Blocks
        # data = {
        #     'transactionID': '1',
        #     'sender': 'akolo',
        #     'receiver': 'Jonah',
        #     'amount': '40',
        #     'token': '5',
        # }
        # for _ in range(3):
        #     r = requests.get(mother + 'pool', json=json.dumps(data))
        #     print('test upload:', r)
        # ## End of Upload Test Blocks
        self.mother = mother
        self.public_key = ''
    
    def blockCount(self) -> int:
        r = requests.get(self.mother + 'blockcount')
        assert r.status_code == 200
        return r.json()['blocks']
    
    def getBlock(self, index) -> dict:
        r = requests.get(self.mother + f'getblock/{index}')
        print(r.status_code)
        assert r.status_code == 200
        return r.json()
    
    def getChain(self, postion:str):
        '''
        get the blockchain (ledger)
        
        position: str
            can range from -1 to infinity
            -1: all the transaction blocks(complete history/ledger)
            0-infinity: the specific block
        '''
        pass

    
    def getDifficulty(self) -> int:
        '''
        get difficulty from server
        '''
        pass
    
    def getCurrentHash(self) -> str:
        '''
        get last uploaded block's hash
        '''
        pass

    def getHash(self, block) -> str:
        '''
        compute the hash of the current block 
        '''
        order = ('time', 'difficulty', 'verifier', 'previousHash')
        nonce = 0
        pass

    def blocksVerified(self, block):
        pass

    def summitMinnedBlock(self, block):
        pass
    
    def mineBlock(self, index):
        block = self.getBlock(index)
        block = self.blocksVerified(block)
        block['time'] = datetime.now().strftime("%I:%M%p %B %d %Y")
        block['difficulty'] = self.getDifficulty()
        block['verifier'] = self.public_key
        block['previousHash'] = self.getCurrentHash()
        (block['hash'], nonce) = self.getHash(block)
        block['nonce'] = nonce
        self.summitMinnedBlock(block)


if __name__ == '__main__':
    
    node = FirstNode("http://127.0.0.1:5000/")
    print("total unprocessed block:", node.blockCount())
    print("\n")
    print("block index=1: ", node.getBlock(0))
    print("block received sucessfully!")
