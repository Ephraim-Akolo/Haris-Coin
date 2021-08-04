import json
from child import Child
from os import system
import rsa
motherAddress = "http://127.0.0.1:5000/"

with open('C:/Users/Ephraim/Desktop/vscode/BlockChain/Harris-Coin/keys.json', 'r') as file:
    keys = json.load(file)
    private_key = keys['private0'].encode('utf-8')
    public_key = keys['public0'].encode('utf-8')

system(f'title serverAcount(public0)')

if __name__ == "__main__":
    childNode = Child(motherAddress)
    transactionID = 1
    print('mother connection status:',childNode.status)
    while True:
        system('cls')
        print('Name: public0',end='\n\n')
        command = input('Enter "send coin", "check balance", "show public key", "show private key", "generate keys" or "exit" command\nCOMMAND: ')
        if command.lower() == 'send coin':
            amount = input('Amount (HRC): ')
            receiver = keys[input('Receiver key: ')]
            data = {
                'transactionID': str(transactionID),
                'sender': {'private': private_key, 'public': public_key},
                'receiver': receiver,
                'amount': str(amount)
            }
            print('sending...')
            d = childNode.send(data)
            transactionID += 1
            print('sent sucessfully!')
            print(d)
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'check balance':
            balance = childNode.checkBalace(public_key.decode("utf-8"))
            print(f'Balance from Nework: {balance}')
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'exit':
            break
        elif command.lower() == 'show public key':
            print('MY PUBLIC KEY: ', (public_key[31:-30]))
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'show private key':
            print('MY PRIVATE KEY: ', (private_key[30:-29]))
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'generate keys':
            (new_private_key, new_public_key) = rsa.newkeys(1024)
            print('Private Key (KEEP SECRET):\n\n', new_private_key.save_pkcs1('PEM').decode("utf-8"))
            input('\npress enter key to get public key...')
            system('cls')
            print('Public Key (serve as public address):\n\n', new_public_key.save_pkcs1('PEM').decode("utf-8"))
            input('\npress enter key...')
            system('cls')
        else:
            print('INVALID COMMAND!')
            input('\npress enter key...')
            system('cls')




