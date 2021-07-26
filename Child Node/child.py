from hashlib import sha256
import requests
import json
import rsa

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
    
    def signature(self, hashToSign:str, privateID:bytes) -> str:
        '''
        Use the public id in 'publicID' to Encrypt the data in 'appendedData'
        and returns the signed data.
        '''
        h = hashToSign.encode('utf-8')
        _key = rsa.PublicKey.load_pkcs1(privateID) # PublicKey function serve as Private key
        return rsa.encrypt(h, _key).decode('ISO-8859-1')

    def sign(self, data:dict) -> str:
        '''
        Digitally signs the appended values of the dictionary of the sender
        to show that the transaction was truely approved by the sender
        '''
        order = ('transactionID', 'sender', 'receiver', 'amount', 'token')
        # copy the sender(private key)
        sender = data['sender']['private']
        # Append and hash the data
        appendedData = sha256()
        for value in order:
            if value == 'sender':
                appendedData.update(data['sender']['public'])
                continue
            appendedData.update(data[value].encode('utf-8'))
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
            assert type(object) == str or type(object) == dict

        # Update and Sign data
        signedData = {
            'id': data['transactionID'],
            'sender': data['sender']['public'].decode('utf-8'),
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

        
