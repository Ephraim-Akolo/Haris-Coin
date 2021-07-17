import requests
import json

class Child:
    def __init__(self, mother:str) -> None:
        '''
        Sends sign's and sends data to Mother Node.

            mother: str
                address of the mother node
        '''
        self._status = False
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

    def sign(self, data:dict):
        signature = None
        return signature

    def send(self,data:dict):
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
        assert len(data) == 5
        for object in data.values():
            assert type(object) == str

        # Update and Sign data
        signedData = {
            'sender': data["sender"],
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

        