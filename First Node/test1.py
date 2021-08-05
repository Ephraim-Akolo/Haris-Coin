from first import FirstNode
from os import system
import json

with open(".\keys.json", 'r') as file:
    keys = json.load(file)
    private_key = keys['private4'].encode('utf-8')
    public_key = keys['public4'].encode('utf-8')

if __name__ == '__main__':
    system('cls')
    node = FirstNode("https://jakeephraim.pythonanywhere.com/", public_key)
    while True:
        print('Name: public4',end='\n\n')
        command = input('Enter "mine block", "available blocks", "balance", "show public key", "show private key", "show chain", "update chain"  or "exit" command\nCOMMAND: ')
        if command.lower() == 'balance':
            balance = node.checkBalace(public_key.decode("utf-8"))
            print(f'Balance from Nework: {balance}')
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'show chain':
            print(node.CHAIN)
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'update chain':
            node.getChain('all')
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'available blocks':
            r = node.blockCount()
            print(f'Unprocessed block{"s" if r > 1 else ""}: ', r)
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'mine block':
            index = int(input('please input index of block starting from zero: '))
            print('minning block...')
            node.mineBlock(index)
            print('Minning successful!: ')
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
