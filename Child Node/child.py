from hashlib import sha256
import requests
import json

class Child:
    def __init__(self, mother:str) -> None:
        '''
        sign's and sends data to Mother Node.

            mother: str
                address of the mother node
        '''
        self._status = False
        self._expectedDictSize = 5
        assert type(mother) == str
        self.mother = mother
        self.testMother()
    
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, a):
        raise ValueError("attempting to set status!!!")

    def testMother(self):
        r = requests.get(self.mother)
        if r.status_code == 200 and r.text == 'OK':
            self._status = True
            return
        self._status = r.status_code
    
    def signature(self, hashToSign:str, publicID:str) -> str:
        '''
        Use the public id in 'publicID' to Encrypt the data in 'appendedData'
        and returns the signed data.
        '''
        return hashToSign

    def sign(self, data:dict) -> str:
        '''
        Digitally signs the appended values of the dictionary with the public key
        of the sender to show that the transaction was truely approved by the sender
        '''
        # copy the sender(public key)
        sender = data['sender']
        # Append and hash the data
        appendedData = sha256()
        for values in data.values():
            appendedData.update(values.encode('utf-8'))
        # sign the hash with the sender(public key) and return
        return self.signature(appendedData.hexdigest(), sender) 

    def send(self,data:dict) -> dict:
        '''            
        data: dict
            sender: str
                public address of the sender
            receiver: str
                public address of the receiver
            amount: str
                amount to transfer from sender to receiver
            token: str
                amount to transfer from sender to first node (transaction fees)
        '''
        assert type(data) == dict
        assert len(data) == self._expectedDictSize
        for object in data.values():
            assert type(object) == str

        # Update and Sign data
        signedData = {
            'id': data['transactionID'],
            'sender': data['sender'],
            'receiver': data['receiver'],
            'amount': data['amount'],
            'token': data['token'],
            'signature': self.sign(data)
        }

        # Send data to the mother pool
        r = requests.get(self.mother + "pool", json=json.dumps(signedData))
        dict_ = r.json()
        dict_['status_code'] = r.status_code
        return dict_

        
