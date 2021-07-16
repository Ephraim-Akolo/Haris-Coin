import requests

def sign(data:dict):
    signature = None
    return signature

def send(mother:str, data:dict):
    '''
    Sends sign's and sends data to Mother Node.

        mother: str
            address of the mother node
        
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
    assert len(data) == 4
    assert type(mother) == str
    for object in data.values, :
        assert type(object) == str
    signedData = {
        'sender': data.sender,
        'receiver': data.receiver,
        'amount': data.amount,
        'token': data.token,
        'signature': sign(data)
    }

    
