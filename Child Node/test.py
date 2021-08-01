from rsa.key import PublicKey
from child import Child
import rsa

(private_key, public_key) = rsa.newkeys(1024)
(sender_private_key, sender_public_key) = rsa.newkeys(1024)
motherAddress = "http://127.0.0.1:5000/"

if __name__ == "__main__":
    childNode = Child(motherAddress)
    transactionID = 1
    print('mother connection status:',childNode.status)
    amount = 40
    print(f'sending {amount}HRC to ', rsa.PublicKey.save_pkcs1(sender_private_key, 'PEM').decode('utf-8'))
    print(f'sender address: {rsa.PublicKey.save_pkcs1(private_key, "PEM").decode("utf-8")}')
    data = {
        'transactionID': str(transactionID),
        'sender': {'private': rsa.PublicKey.save_pkcs1(private_key, 'PEM'), 'public': rsa.PrivateKey.save_pkcs1(public_key, 'PEM')},
        'receiver': rsa.PublicKey.save_pkcs1(sender_private_key, 'PEM').decode('utf-8'),
        'amount': str(amount),
        'token': '5',
    }
    d = childNode.send(data)
    print('sent sucessfully!')
    print(d)



