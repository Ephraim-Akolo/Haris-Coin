from child import Child
motherAddress = "http://127.0.0.1:5000/"

if __name__ == "__main__":
    childNode = Child(motherAddress)
    transactionID = 1;
    print(childNode.status)
    data = {
        'transactionID': str(transactionID),
        'sender': 'Akolo',
        'receiver': 'Jonah',
        'amount': '40',
        'token': '5',
    }
    d = childNode.send(data)
    print(d)



