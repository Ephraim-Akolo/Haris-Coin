from rsa.key import PublicKey
from child import Child
import rsa

(private_key, public_key) = rsa.newkeys(1024)
motherAddress = "http://127.0.0.1:5000/"

if __name__ == "__main__":
    childNode = Child(motherAddress)
    transactionID = 1
    print(childNode.status)
    data = {
        'transactionID': str(transactionID),
        'sender': {'private': rsa.PublicKey.save_pkcs1(private_key, 'PEM'), 'public': rsa.PrivateKey.save_pkcs1(public_key, 'PEM')},
        'receiver': 'Jonah',
        'amount': '40',
        'token': '5',
    }
    d = childNode.send(data)
    print(d)



