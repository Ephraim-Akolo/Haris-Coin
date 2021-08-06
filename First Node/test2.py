from first import FirstNode
from os import system
import json
import rsa

with open(".\keys.json", 'r') as file:
    keys = json.load(file)
    private_key = keys['private3'].encode('utf-8')
    public_key = keys['public3'].encode('utf-8')

if __name__ == '__main__':
    node = FirstNode("https://jakeephraim.pythonanywhere.com/", public_key)
    while True:
        system('cls')
        print('Name: public3',end='\n\n')
        command = input('Enter "mine block", "available blocks", "show block", "balance", "show public key", "show private key", "show chain", "update chain"  or "exit" command\nCOMMAND: ')
        if command.lower() == 'balance':
            balance = node.checkBalace(public_key.decode("utf-8"))
            print(f'Balance from Nework: {balance}')
            input('\npress enter key...')
            system('cls')
        elif command.lower() == 'show chain':
            chain = node.CHAIN
            size = 'size'
            order = ('time', 'difficulty', 'verifier', 'token', 'previousHash', 'nonce', 'hash')
            print('\nCHAIN SIZE: ', chain[size], end='\n\n')
            for n in range(chain[size]):
                block = chain[str(n)]
                print('BLOCK ', n+1)
                for obj in order:
                    if obj == 'verifier':
                        print(obj,'(index 32-52): ', block[obj][32:52])
                        continue
                    print(obj,': ', block[obj])
                print()
            input('\n\npress enter key...')
            system('cls')
        elif command.lower() == 'show block':
            chain = node.CHAIN
            size = 'size'
            n = int(input('block index: '))
            block = chain[str(n-1)]
            for k in range(block[size]):
                trans = block[str(k)]
                print('\n\nSENDER (index 32-92): ', trans['sender'][32:92])
                print('RECEIVER (index 32-92): ', trans['receiver'][32:92])
                print('AMOUNT (index 32-92): ', trans['amount'])
                print('SIGNATURE[fingerprint] (index 32-92): ', trans['signature'][32:92], end='\n')
            input('\n\npress enter key...')
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
            print('Private Key (KEEP SECRET):\n\n', new_private_key.save_pkcs1('PEM'))
            input('\npress enter key to get public key...')
            system('cls')
            print('Public Key (serve as public address):\n\n', new_public_key.save_pkcs1('PEM'))
            input('\npress enter key...')
            system('cls')
        else:
            print('INVALID COMMAND!')
            input('\npress enter key...')
            system('cls')
