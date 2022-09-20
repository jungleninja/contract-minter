import sys
import time
from web3 import Web3

W3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b68c55096e8e42f98417020ce8a0eb28'))

MY_ADDR = W3.toChecksumAddress('0x7Ac4efdB22702322dDadcf742Bb512A52AbF24CB')        # your address
MY_PRIVATE_KEY = 'xxx' # your private key

abi='''
[
    { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "inputs": [ { "internalType": "uint256", "name": "times", "type": "uint256" }, { "internalType": "address", "name": "_addr", "type": "address" }, { "internalType": "bytes", "name": "_data", "type": "bytes" } ], "name": "batchCall", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "target", "type": "address" } ], "name": "clone", "outputs": [ { "internalType": "address", "name": "result", "type": "address" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_num", "type": "uint256" } ], "name": "deploySubAddrs", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_user", "type": "address" } ], "name": "getSubaddress", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" }, { "internalType": "address[]", "name": "", "type": "address[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_user", "type": "address" }, { "internalType": "address", "name": "_token", "type": "address" } ], "name": "getSubaddressAndTokenids", "outputs": [ { "internalType": "address[]", "name": "", "type": "address[]" }, { "internalType": "uint256[][]", "name": "", "type": "uint256[][]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "", "type": "address" }, { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "subAddressList", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "subcontract", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "withdrawETHEmergency", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_token", "type": "address" }, { "internalType": "address", "name": "_to", "type": "address" } ], "name": "withdrawNFTs", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_token", "type": "address" }, { "internalType": "address", "name": "_to", "type": "address" }, { "internalType": "address[]", "name": "_subaddrs", "type": "address[]" }, { "internalType": "uint256[][]", "name": "_tokenids", "type": "uint256[][]" } ], "name": "withdrawNFTsV2", "outputs": [], "stateMutability": "nonpayable", "type": "function" }
]
'''
contract = W3.eth.contract(address=W3.toChecksumAddress('0xED44409de91A340df26667E1FD21C9DA1EdE0Ef1'), abi=abi) # contract minter address  

abi_query = [ { "inputs": [ { "internalType": "address[]", "name": "_subaddress", "type": "address[]" }, { "internalType": "address", "name": "_nftaddr", "type": "address" } ], "name": "query", "outputs": [ { "internalType": "address[]", "name": "", "type": "address[]" }, { "internalType": "uint256[][]", "name": "", "type": "uint256[][]" } ], "stateMutability": "view", "type": "function" } ]
query_contract = W3.eth.contract(address=W3.toChecksumAddress('0x30d9C5533AD3e3ca3174166b76AEB84C29f633c3'), abi=abi_query)

MENU = '''
--------------------
  contract minter 
    Xinja#8947
--------------------
1. deploy subaddress
2. show all your subaddress
3. mint NFTs
4. withdraw NFTs 
5. exit
--------------------
'''

def send_raw_transaction(ts):
    W3.eth.call(ts)
    signed_txn = W3.eth.account.sign_transaction(ts, MY_PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"tx_hash: {W3.toHex(tx_hash)} , please wait for a while to get the receipt")
    receipt = W3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"tx confirmed in block {receipt['blockNumber']}, status: {receipt['status'] == 1}, gas cost {round(W3.fromWei(receipt['gasUsed'] * receipt['effectiveGasPrice'], 'ether'), 4)} ETH ")

def auto_speedup(ts,maxgasprice):
    W3.eth.call(ts)
    signed_txn = W3.eth.account.sign_transaction(ts, MY_PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"tx_hash: {W3.toHex(tx_hash)} , gasprice {W3.fromWei(ts['maxFeePerGas'], 'gwei')} gwei, max priority fee {W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei')} gwei")
    while True:
        receipt = W3.eth.getTransaction(tx_hash)
        if receipt['blockNumber'] != None:
            receipt = W3.eth.get_transaction_receipt(tx_hash)
            print(f"tx {W3.toHex(tx_hash)} confirmed in block {receipt['blockNumber']}, status: {receipt['status'] == 1}, gas cost {round(W3.fromWei(receipt['gasUsed'] * receipt['effectiveGasPrice'], 'ether'), 4)} ETH ")
            break
        else:
            gasprice = W3.eth.gas_price
            if gasprice < maxgasprice and gasprice - ts["maxFeePerGas"] > W3.toWei(1, 'gwei'):
                gasprice1 = gasprice + W3.toWei(1, 'gwei')
                gasprice2 = ts['maxFeePerGas'] * 1.101
                if gasprice1 > gasprice2:
                    ts['maxFeePerGas'] = gasprice1
                else:
                    ts['maxFeePerGas'] = gasprice2
                ts['maxPriorityFeePerGas'] = W3.eth.max_priority_fee
                signed_txn = W3.eth.account.sign_transaction(ts, MY_PRIVATE_KEY)
                tx_hash = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print(f"speedup tx_hash: {W3.toHex(tx_hash)} , gasprice {W3.fromWei(ts['maxFeePerGas'], 'gwei')} gwei, max priority fee {W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei')} gwei")
        time.sleep(0.5)

    

def deploy_subaddress():
    num = int(input("how many subaddress do you want to deploy? >>> "))
    nonce = W3.eth.getTransactionCount(MY_ADDR)
    params = {
        'from': MY_ADDR,
        'chainId': W3.toHex(W3.eth.chain_id),
        'value': W3.toHex(0),
        'nonce': W3.toHex(nonce)
    }
    ts = contract.functions.deploySubAddrs(num).buildTransaction(params)
    gas_cost = W3.fromWei((ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']) * ts['gas'], 'ether')
    print(f"max gas cost: {round(gas_cost, 4)} ETH (gas price: {round(W3.fromWei(ts['maxFeePerGas'], 'gwei'), 2)} gwei, max priority fee: {round(W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei'), 2)} gwei, gas limit: {ts['gas']})")
    ans = input("do you want to continue? (y/n) >>> ")
    if ans == 'y':
        send_raw_transaction(ts)
    else:
        ans = input("custom gas price? (y/n) >>> ")
        if ans == 'y':
            gasprice = float(input("gas price (gwei) >>> "))
            maxpriorityfee = float(input("max priority fee (gwei) >>> "))
            ts['maxFeePerGas'] = W3.toWei(gasprice, 'gwei')
            ts['maxPriorityFeePerGas'] = W3.toWei(maxpriorityfee, 'gwei')
            gas_cost = W3.fromWei((ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']) * ts['gas'], 'ether')
            block = W3.eth.get_block('latest')
            basefee = block['baseFeePerGas']
            print(f"max gas cost: {round(gas_cost, 4)} ETH (gas price: {round(W3.fromWei(ts['maxFeePerGas'], 'gwei'), 2)} gwei, max priority fee: {round(W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei'), 2)} gwei, gas limit: {ts['gas']})")
            if ts['maxFeePerGas'] < basefee:
                print(f"gas price too low, base fee: {round(W3.fromWei(basefee, 'gwei'), 2)} gwei")
                w = input("do you want to wait for the block basefee to be less than your gas price and auto send transaction? (y/n) >>> ")
                if w == 'y':
                    print("press ctrl+c to stop")
                    while True:
                        try:
                            block = W3.eth.get_block('latest')
                            basefee = block['baseFeePerGas']
                            print(f"block {block['number']} base fee: {round(W3.fromWei(basefee, 'gwei'), 2)} gwei \nrefersh in 2 seconds...", end='\r')
                            if ts['maxFeePerGas'] >= basefee:
                                send_raw_transaction(ts)
                                break
                            time.sleep(2)
                        except KeyboardInterrupt:
                            print("\nstopped")
                            break
            else:
                ans = input("do you want to continue? (y/n) >>> ")
                if ans == 'y':
                    send_raw_transaction(ts)

def show_subaddress():
    print("fetching your subaddress...")
    subaddrs = contract.functions.getSubaddress(MY_ADDR).call()
    for i, addr in enumerate(subaddrs[1]):
        print(f"{i+1}: {addr}")

def mint_nfts():
    menu = '''
    1. mint NFTs by hash
    2. mint NFTs by hexdata
    '''
    print(menu)
    ans = int(input("Enter your choice: "))
    if ans == 1:
        hash = input("please input the hash >>> ")
        tx = W3.eth.getTransaction(hash.replace(' ', ''))
        hexdata = tx['input']
        to = tx['to']
        value = tx['value']
    elif ans == 2:
        hexdata = input("please input the hexdata >>> ")
        to = W3.toChecksumAddress(input("please input the NFTs contract address >>> "))
        value = input("please input the price >>> ")
        value = W3.toWei(value, 'ether')
    else:
        print("invalid input")
        return
    num = int(input("please input how many subaddress you want to mint >>> "))
    print(f"use {num} subaddress to mint NFTs need {W3.fromWei(value * num, 'ether')} ETH")
    nonce = W3.eth.getTransactionCount(MY_ADDR)
    params = {
        'from': MY_ADDR,
        'chainId': W3.toHex(W3.eth.chain_id),
        'value': W3.toHex(value * num),
        'nonce': W3.toHex(nonce)
    }
    ts = contract.functions.batchCall(num, to, hexdata).buildTransaction(params)
    gas_cost = W3.fromWei((ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']) * ts['gas'], 'ether')
    print(f"max gas cost: {round(gas_cost, 4)} ETH (gas price: {round(W3.fromWei(ts['maxFeePerGas'], 'gwei'), 2)} gwei, max priority fee: {round(W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei'), 2)} gwei, gas limit: {ts['gas']})")
    ans = input("do you want to continue? (y/n) >>> ")
    if ans == 'y':
        ans = input("enable auto speedup? (y/n) >>> ")
        if ans == 'y':
            max_gasprice = float(input("max gas price (gwei) >>> "))
            auto_speedup(ts, max_gasprice)
        else:
            send_raw_transaction(ts)
    else:
        ans = input("custom gas price? (y/n) >>> ")
        if ans == 'y':
            gasprice = float(input("gas price (gwei) >>> "))
            maxpriorityfee = float(input("max priority fee (gwei) >>> "))
            ts['maxFeePerGas'] = W3.toWei(gasprice, 'gwei')
            ts['maxPriorityFeePerGas'] = W3.toWei(maxpriorityfee, 'gwei')
            gas_cost = W3.fromWei((ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']) * ts['gas'], 'ether')
            print(f"max gas cost: {round(gas_cost, 4)} ETH (gas price: {round(W3.fromWei(ts['maxFeePerGas'], 'gwei'), 2)} gwei, max priority fee: {round(W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei'), 2)} gwei, gas limit: {ts['gas']})")
            ans = input("do you want to continue? (y/n) >>> ")
            if ans == 'y':
                send_raw_transaction(ts)

def withdraw_nfts():
    nft_addr = W3.toChecksumAddress(input("please input the NFTs contract address >>> "))
    print("fetching your NFTs...")
    res = [[],[]]
    subaddrs = contract.functions.getSubaddress(MY_ADDR).call()[1]
    res = query_contract.functions.query(subaddrs, nft_addr).call()
    subaddrs = res[0]
    tokenids = res[1]

    subaddrs = [subaddrs[i] for i, tokenid in enumerate(tokenids) if tokenid]
    tokenids = [tokenid for tokenid in tokenids if tokenid]

    total = 0
    for i in tokenids:
        total += len(i)
    if total == 0:
        print("you don't have this NFTs")
        return
    print(f"you subaddress has total of {total} of this NFTs")
    menu = '''
    1. withdraw to your address
    2. withdraw to other address
    '''
    print(menu)
    ans = int(input("Enter your choice: "))
    if ans == 1:
        to = MY_ADDR
    elif ans == 2:
        to = W3.toChecksumAddress(input("please input the address >>> "))
    else:
        print("invalid input")
        return
    num = int(input("please input how many NFTs you want to withdraw >>> "))
    if num > total:
        num = total
    atindex = 0
    tmp = 0
    for i in tokenids:
        tmp = tmp + len(i)
        if tmp >= num:
            atindex = tokenids.index(i)
            break
    tokenids = tokenids[:atindex+1]
    subaddrs = subaddrs[:atindex+1]
    nonce = W3.eth.getTransactionCount(MY_ADDR)
    params = {
        'from': MY_ADDR,
        'chainId': W3.toHex(W3.eth.chain_id),
        'nonce': W3.toHex(nonce)
    }
    ts = contract.functions.withdrawNFTsV2(nft_addr, to, subaddrs, tokenids).buildTransaction(params)
    gas_cost = W3.fromWei((ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']) * ts['gas'], 'ether')
    print(f"max gas cost: {round(gas_cost, 4)} ETH (gas price: {round(W3.fromWei(ts['maxFeePerGas'], 'gwei'), 2)} gwei, max priority fee: {round(W3.fromWei(ts['maxPriorityFeePerGas'], 'gwei'), 2)} gwei, gas limit: {ts['gas']})")
    ans = input("do you want to continue? (y/n) >>> ")
    if ans == 'y':
        send_raw_transaction(ts)

def main():
    while True:
        try:
            print(MENU)
            choice = int(input('Enter your choice: '))
            if choice == 1:
                deploy_subaddress()
            elif choice == 2:
                show_subaddress()
            elif choice == 3:
                mint_nfts()
            elif choice == 4:
                withdraw_nfts()
            elif choice == 5:
                break
            else:
                print('Invalid choice')
        except Exception as e:
            print(f"error: {e}")

if __name__ == "__main__":
    if W3.isConnected():
        main()
    else:
        print("web3 connection error, please check your provider")
