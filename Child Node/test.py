import json

from requests.api import delete
from child import Child

# (private_key, public_key) = rsa.newkeys(1024)
# (sender_private_key, sender_public_key) = rsa.newkeys(1024)

with open('C:/Users/Ephraim/Desktop/vscode/BlockChain/Harris-Coin/keys.json', 'r') as file:
    keys = json.load(file)
    private_key = keys['private0'].encode('utf-8')
    public_key = keys['public0'].encode('utf-8')
    receiver = keys['public2']
    keys = ''

motherAddress = "http://127.0.0.1:5000/"

if __name__ == "__main__":
    childNode = Child(motherAddress)
    transactionID = 1
    print('mother connection status:',childNode.status)
    amount = 40
    print(f'sending {amount}HRC to: ', receiver)
    print(f'sender address: {public_key.decode("utf-8")}')
    data = {
        'transactionID': str(transactionID),
        'sender': {'private': private_key, 'public': public_key},
        'receiver': receiver,
        'amount': str(amount)
    }
    d = childNode.send(data)
    print('sent sucessfully!')
    print(d)



