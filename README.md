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
The mother node by nature is server which is hosted online for all nodes to access. All nodes in the network communicate through the server. The server comprises of pool and block chain. The pool is where the child nodes send their transaction details that have been signed and in Json format to mother for processing and to be added to the block chain by the first node. The block chain is just an open ledger where preceding transaction block is connected to a previous hash by a reference hash found through a concept known as prove of work. The unprocessed transactions are currently grouped in hundred’s called the unprocessed block. The first node can request for any available unprocessed block to verify the signature and transaction to confirm it was not faked then process it and return it to the mother to be added to the block chain. The first node to complete the processing and verification task gets the token for all the transactions in the unprocessed block.
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
  
### THE FIRST NODE
This can also be referred to the mining or verification node. This node is just as the child node but with extra abilities. This node is able to query the mother node like the child node, but unlike the child node, it is able to request for unprocessed transaction block and verify that the decoded hash matches the hashed data. The hash Algorithm used is the SHA256 algorithm, which takes any given length of data and converts it to a fixed unique 256 byte length of data. No two hashes are similar even on the lightest omission of data. The first node takes the transactions in the block and verifies them one by one. The node first verify in the chain if the sender has enough coins to send, and also confirms other information. It then creates a hash of the data and decode the signature using the sender address which is the public key, it then compares the two hashes and approve it as valid, if the hashes are the same. It then creates an appended string of the current data and the previous block hash on the block chain and perform a sequence of operation known as “prove of work”. This prove of work is  a term that explains when a computer resources is used to perform work in guessing a number (called nonce) that when added to the hash data, it gives a new hexadecimal hash starting with a certain number of preceding zero’s. This new hash will become the blocks hash and will be used by the next block to be placed to from a chain of hashes.
Some function currently in the first node python script includes:
  
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
  
* mineBlock(index) -> str:__ This is the function that triggers the mining sequence. It takes the index of the pool block to mine and assignes the workload to the respective functions.
  
## Transactions
A child node transfer the coin to the next child node by signing the transaction details with the public key of the next child node, so that the next child node can verify the transaction was made to it by its signed public key. The transactions block can be added to the chain by hashing the previous hash and the current block with a certain difficulty. The block is then broadcasted to the mother node and first nodes for verification before being added to the chain. The transaction with next transaction id is considered first and if the next transaction's id does not match the next, it is negleted.
