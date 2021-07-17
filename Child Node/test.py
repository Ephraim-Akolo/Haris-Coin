from child import Child
motherAddress = "http://127.0.0.1:5000/"

if __name__ == "__main__":
    childNode = Child(motherAddress)
    print(childNode.status)
    data = {
        'sender': 'Akolo',
        'receiver': 'Jonah',
        'amount': '40',
        'token': '5',
        'key': 'akolojonahkutsa'
    }
    d = childNode.send(data)
    print(d)



