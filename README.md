# Haris Coin: A Transparent Centralized Electronic Cash System
## Abstract:
This electronic cash will try to solve governmental issues towards crypto currency as they cannot be regulated or accounted for, while still maintaining the blockchain’s open ledger and a level of anonymity. Most attributes of cyptocurrency are maintained except the network is centralized, such that, the “mother node” with power to distribute the coin from her reserves is control by a centralized body unlike other crypto currencies which can be mined to put the coin in circulation. Like bitcoin, the network processes signed transaction by hashing them into an ongoing chain of hash-based proof-of-work, forming a record that cannot be changed without redoing the proof-of-work. Nodes communicate with the mother on demand, accepting the Mothers node Proof-of-work chain as proof of what happened while they were away.
## Introduction:
Haris Coin is a transparent digital currency based on blockchain technology in which everyone in the network has access to the blockchain and all its data. It is a network of three (3) different types of nodes namely: 
* Mother Node
* First Node
* Child Node.

![Haris Network](data/HRC-Network.png)

### THE MOTHER NODE
The mother node by nature is server which is hosted online for all nodes to access. All nodes in the network communicate through the server. The server comprises of pool and block chain. The pool is where the child nodes send their transaction details that have been signed and in Json format to mother for processing and to be added to the block chain by the first node. The block chain is just an open ledger where preceding transaction block is connected to a previous hash by a reference hash found through a concept known as prove of work. The unprocessed transactions are currently grouped in hundred’s called the unprocessed block. The first node can request for any available unprocessed block to verify the signature and transaction to confirm it was not faked then process it and return it to the mother to be added to the block chain. The first node to complete the processing and verification task gets the token for all the transactions in the unprocessed block. The mother node gets 25% of the token for every transaction.
Functions offered by the mother noded include

* __index ([/](https://jakeephraim.pythonanywhere.com/)) -> 'OK':__ This is the home route of the server. it only function is to confirm connection to the sever and it returns “OK” as a string.

* __pool (/pool, json=DATA) -> {'in_pool': True|False}:__ This is the route where the child node sends it transaction log or details in a Json format. The function takes the Json object and add it to the Unprocessed block in the pool. When successful, the function returns a Json or Python Dictionary object with “in_pool” set to “True”. Below is and example of the DATA format.
  DATA = {
            'transactionID': transaction id in "utf-8" fomat,
            'sender': sender's hexadecimal public key in "utf-8" fomat,
            'receiver': receiver's hexadecimal public key in "utf-8" fomat ,
            'amount': amount to send in "utf-8" format,
            'signature': signature in "ISO-8859-1" format
         }
          
* __getBlock ([/getblock/<index>](https://jakeephraim.pythonanywhere.com/getblock/1)) -> DATA:__ This route is used to query the server by the first node and requests for a certain block of unprocessed transaction to process. The server returns a Json or Python Dictionary of the required block of unprocessed data not yet added to the chain. Below is and example of the DATA format returned.
  DATA = {
            'transactionID': transaction id in "utf-8" fomat,
            'sender': sender's hexadecimal public key in "utf-8" fomat,
            'receiver': receiver's hexadecimal public key in "utf-8" fomat ,
            'amount': amount to send in "utf-8" format,
            'signature': signature in "ISO-8859-1" format
         }
  
* __blockCount([/blockcount](https://jakeephraim.pythonanywhere.com/blockcount)) -> {"blocks": <number>}:__ This route is used to query the server on the available blocks of unprocessed data. It returns a Json or Python Dictionary format with “blocks” set to the number of unprocessed blocks on the server

* __getChain([/getchain/<position>](https://jakeephraim.pythonanywhere.com/getchain/all)) -> CHAIN:__ This route is used to query the server to get all or part of the chain (ledger). it returns a block of transactions in the ledger when position is a number, and the entire chain or blocks when position is -1 or "all". 

* __getDifficulty([/getdifficulty](https://jakeephraim.pythonanywhere.com/getdifficulty)) -> {"difficulty": number}:__ This route is used to query the server to get the set difficulty of the network by the mother node. It returns json with "difficulty" set to a number.
  
* __getToken([/gettoken](https://jakeephraim.pythonanywhere.com/gettoken)) -> {"token": number}:__ This route is used to query the server to get the set token by the mother node. The token is simply the transaction fee paid to send the coin.
  
* __isMother(/motherkey, json={"key": public key}) -> {"ismother": True|False}:__ This route is used to query the mother node or server if the key passed in json format is the mother public key. Returns a json object with "ismother" set to True or False.
  
* __getCurrentHash([/getcurrenthash](https://jakeephraim.pythonanywhere.com/getcurrenthash)) -> {"hash": last block hash}:__ This route is used to query the server for the last blocks hash value. It returns a json object with "hash" value set to the hash of the last block in the chain.

* __summitMinnedBlock(/summitminnedblock, json=MINED_DATA) -> {"submit_status": True|False, "Error": Message}:__ This route is used to submit mined and verified blocks of transaction (MINED_DATA) to the server in json format to be added to the chain. The MINED_DATA must contain the time, difficulty(gotten from server), verifier public key, token (gotten form server), previous hash (gotten from server as current hash), nonce which is the prove of work, and the new current hash. The mother node verifies that this data was truely mined by verifying the proof of work. This is done by appending or concatinating the string value of the above first five data and finally with the nonce(proof of work), to get a string of data which can be encoded to a byte format and hashed using the sha256 to a hexadecimal string which is then compared with the hash in the block. The prove of work is true if the verified hash matches the block hash and also begins with a leading number of zero specified by the difficulty requirement.
  
### THE CHILD NODE
The child node is just a client of the mother node (main server). This node is node is only able a access the block chain or the open ledger which is open to everyone, and also place transactions (such as send and receive coins) in the mother pool. To send and receive coins, one must obtain a public and private keys in which the public key serves as the address to the wallet of the child and also serves as a means for the “first node” to be able to verify all transaction was authorize by the child node. The private key serves as the password to send coins and also as a means to sign or create an encrypted version of the transaction called the unique fingerprint. The private key signs transactions and the public key is used to verify the transaction signed by the private key. The public and private key is generated using the RSA Module which uses the principle of the “trap door algorithm”, which can encode data with the private key and can only be decoded with the corresponding public key. The hash algorithm is a one way algorithm that converts a given data to a fixed length byte code or hexadecimal. Some function currently in the child node python script includes:
  
* __testMother() -> status_code:__ This function is used to test the connection to the “mother node” or main server. The connection is successful if a response code of 200 is received and the server replies “OK”

* __signature(hashToSign, Private_key) -> string:__ This function takes the hash of the data and the private key, then returns an encrypted version of the hash called the fingerprint decoded to a string in the 'ISO-8859-1' format which can be decrypted with the public key.
  
* __sign(data) -> string:__ This function takes the data from the send function and append the data, then creates a hash of the data using the SHA256 algorithm . It then sends the hashed data and the private key to the signature function for encryption or signing. It gets the signed data from signature and then returns it to the send function.  

* __send(data) -> None:__ This function takes the transaction data to be sent to the mother node and trigger the sign function, then sends it to the mother pool where it is added to the unprocessed block. This function receives a dictionary which “in_pool” is  True and a response of 200 from the server.

* __getChain(position) -> dict:__ This function query the mother node or server and return the whole or blocks in ledger or block chain. position can be from zero to infinity to get a certain available block, or -1 or "all" to get the whole available ledger or blockchain. This is automatically triggered in the in the checkBalance function of the child node.
  
* __checkBalance(public_key) -> float:__ This function goes up the blockchain and calculates or gathers the coin belonging to the public key entered. It returns the available coin balance of the public_key.
  
### THE FIRST NODE
This can also be referred to the mining or verification node. This node is just as the child node but with extra abilities. This node is able to query the mother node like the child node, but unlike the child node, it is able to request for unprocessed transaction block and verify that the decoded hash matches the hashed data. The hash Algorithm used is the SHA256 algorithm, which takes any given length of data and converts it to a fixed unique 256 byte length of data. No two hashes are similar even on the lightest omission of data. The first node takes the transactions in the block and verifies them one by one. The node first verify in the chain if the sender has enough coins to send, and also confirms other information. It then creates a hash of the data and decode the signature using the sender address which is the public key, it then compares the two hashes and approve it as valid, if the hashes are the same. It then creates an appended string of the current data and the previous block hash on the block chain and perform a sequence of operation known as “prove of work”. This prove of work is  a term that explains when a computer resources is used to perform work in guessing a number (called nonce) that when added to the hash data, it gives a new hexadecimal hash starting with a certain number of preceding zero’s. This new hash will become the blocks hash and will be used by the next block to be placed to from a chain of hashes.The first node get's 75% of the token for every transaction.Some function currently in the first node python script includes:
  
* __blockCount() -> int:__ This function query the mother node of the available unprocessed blocks of data. The mother node responds with a Json object with “blocks” set to the value of the available blocks of unprocessed or invalidated data. 
* __getBlock(index) -> dict:__ This function query the mother node with and index number of the blocks needed. The mother node responds by sending back the requested block of unprocessed data. The first node can then proceed to validate and process the block of data received.
  
* __getChain(position) -> dict:__ This function query the mother node or server and return the whole or blocks in ledger or block chain. position can be from zero to infinity to get a certain available block, or -1 or "all" to get the whole available ledger or blockchain.

* __getDifficulty() -> str:__ Returns the string format of the difficulty from the server.
  
* __getCurrentHash() -> str:__ Returns the hash of the last block updated in the mother server's blockchain.

* __getHash(block) -> str:__ This is the function which implements the sha256 hash algorithm and mines the block of data.
  
* __checkBalance(public_key) -> float:__ This function goes up the blockchain and calculates or gathers the coin belonging to the public key entered. It returns the available coin balance of the public_key.
  
* __getTokenAmount() -> str:__ Returns the transaction charge from the server or mother node.
  
* __signatureVerified(data) -> bool:__ This function verifies the signature or unique transaction fingerprint and returns True if valid, otherwise it returns false.
  
* __summitMinnedBlock(block, index) -> str:__ This function submits the mined block to the server along with the pool index number.
  
* __mineBlock(index) -> str:__ This is the function that triggers the mining sequence. It takes the index of the pool block to mine and assignes the workload to the respective functions.
  
## Transactions
A child node transfer the coin to the next child node by signing the transaction details with the public key of the next child node inclusive, so that the next child node can verify the transaction was made to it by its signed public key. The transactions block can be added to the chain by hashing the previous hash and the current block data with a certain difficulty. The block is then broadcasted to the mother node and then to the first nodes for verification before being added to the chain. 
### Steps in sending coin from 'A' to 'B'
  * 'A' create's the transaction log as shown below:
      DATA = {
              'transactionID': transaction id in "utf-8" string fomat,
              'sender': sender's hexadecimal public key in "utf-8" string fomat,
              'receiver': receiver's hexadecimal public key in "utf-8" string fomat ,
              'amount': amount to send in "utf-8" string format
            }
  
  * 'A' then signs (hashed using sha256 then encrypted using the private key) all the infomation and attach it to the transaction log before broadcasting it to the public through the mother node as shown below:
      DATA = {
            'transactionID': transaction id in "utf-8" fomat,
            'sender': sender's hexadecimal public key in "utf-8" fomat,
            'receiver': receiver's hexadecimal public key in "utf-8" fomat ,
            'amount': amount to send in "utf-8" format,
            'signature': sign's the value of (transactionID, sender, receiver, amount) and decode it to a string in "ISO-8859-1" format
         }
  
  * 'A' then sends the data as a json format to the pool route of the mother node or server. it is immediately added to a loading block of transactions and accessible to everyone. The coin is not regarded as sent yet because it has not been verified and added to the chain yet.
  
  * First node then take's the block of transactions which has 'A' sending money to 'B', and verifies all the transactions in the block, removing any invalid transaction (may be due to insufficient coin, etc).
  
  * The first node then fill's additional data to the block like: time of transaction, token which is the reward for verifying a block or mining (can be gotten from the server), difficulty (the number of preceeding zero's in the final hexadecimal hash), verifier (which is the public key to pay the token) and the last hash of the last block on the chain.
  
  * The data above is then appended together and a guessed number called the nonce is added to the end of the appended data and hashed using the sha256 algorithm.
  
  * If the value of the appended nonce(guessed number) in the above do not produce a hash that matches the difficulty(a number less than the value with the preceeding number of zero's), another number is guessed until the difficulty is attained. The nonce and the hash(meeting the difficulty requirement) of a block is the prove that work was done(prove of work) on that block.
  
  * The block is then submitted back to the server through the "summitminnedblock" route of the mother as a json object to be added to the chain of blocks (blockchain). But before that, the mother confirms the prove of work by hashing the data appended to the nonce, and if the hash matches the given block hash with the given difficulty requirement, the block is added to chain and it becomes the new current or last block.The blockchain is saved as a json file on the host hard drive.
  
  * The first "first node" to complete the task and send to the server get's 75% of the token of all transaction's in the verified block, and the mother node always get's 25% of every transaction.
  
  * 'B' can now go through the blockchain to see that 'A' at a given recent block signed with its private key the amount of coin and it has been verified and added to the chain. Therefore the coin can be regarded as sent successfully.  
  
