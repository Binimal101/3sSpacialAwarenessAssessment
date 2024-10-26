import json, datetime, os
from web3 import Web3
from web3.exceptions import TransactionNotFound
from dotenv import load_dotenv

load_dotenv()

# Connect to your Google Cloud Sepolia Node
node_url = os.environ.get("GCPBlockchainNode")
w3 = Web3(Web3.LegacyWebSocketProvider(node_url))

#TODO add secrets
account = os.environ.get("SepoliaAccountHash", None)
private_key = os.environ.get("SepoliaAccountPrivateKey", None)

if not account or not private_key:
    print(f"missing account or private key. Make sure .env is configured correctly.")
    quit()

encodeDataForTransmission = lambda data: "0x" + json.dumps(data).encode("utf-8").hex() #gives hexadecimal representation of JSON for block-transaction storage
decodeDataForTraining = lambda data: json.loads(bytes.fromhex(data[2:]).decode("utf-8")) #gives JSON object with encoded data + timestamp

def addBlockToBlockchain(encyrptedJSONData: dict):

    encyrptedJSONData["timestamp"] = datetime.utcnow().timestamp()
    # Homomorphically encrypted JSON data, converted to hex
    encryptedPayload = encodeDataForTransmission(encyrptedJSONData)

    # Prepare the transaction with required fields
    transaction = {
        'to': None,  # Use None if it's only for storing data without sending to a recipient
        'value': 0,  # No ETH transfer, just data storage
        'gas': 50000 + len(encryptedPayload) // 10,  # Adjust gas limit based on data size
        'gasPrice': w3.toWei('10', 'gwei'),  # Example gas price, you can query current price
        'nonce': w3.eth.getTransactionCount(account),
        'chainId': 11155111,  # Chain ID for Sepolia testnet
        'data': encryptedPayload  # Your encrypted JSON data in hex format
    }

    try:
        # Sign and send the transaction
        signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("Uploaded Transaction, hash:", txn_hash.hex())
    except Exception as e:
        print("Error uploading transaction:", e)

def getRecentCKKSTestsFromBlockchain() -> list:
    """
    Returns CKKS data from the latest transaction in latest block in the blockchain
    [
        {
            age
            string-command-omissions
            page-centered-omission
            correct-responses
        },
        {},
        ...
    ]
    """
    try:
        latestBlock = w3.eth.getBlock("latest")

        if not len(latestBlock.transactions):
            return None

        newestTransaction = w3.eth.getTransaction(latestBlock.transactions[0])
        # Loop through each transaction in the block
        for txn_hash in latestBlock.transactions:
            
            # Retrieve transaction details
            transaction = w3.eth.getTransaction(txn_hash)
            
            #find newest transaction
            if decodeDataForTraining(transaction["input"]).get( "timestamp", 0) > decodeDataForTraining(newestTransaction["input"]).get("timestamp", 0):
                newestTransaction = transaction
            
        #newest transaction with encrypted K-Means dataset accessible in newestTransaction["data"]
        returnable = decodeDataForTraining(newestTransaction["input"]) #return JSON representation from hexdigest
        del returnable["timestamp"] #timestamp not needed for training
        
        return returnable["tests"] #return only tests as list
    except TransactionNotFound as e:
        print("Transaction not found error:", e)
        return None
    
    except Exception as e:
        print("Error retrieving CKKS tests:", e)
        return None