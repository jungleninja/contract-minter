from web3 import Web3
from hexbytes import HexBytes

W3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b68c55096e8e42f98417020ce8a0eb28'))

MY_ADDR = W3.toChecksumAddress('0x7Ac4efdB22702322dDadcf742Bb512A52AbF24CB')
MY_PRIVATE_KEY = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'

abi='''
[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "times",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "bytes",
				"name": "_data",
				"type": "bytes"
			}
		],
		"name": "batchCall",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "target",
				"type": "address"
			}
		],
		"name": "clone",
		"outputs": [
			{
				"internalType": "address",
				"name": "result",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_num",
				"type": "uint256"
			}
		],
		"name": "deploySubAddrs",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "getSubaddress",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_token",
				"type": "address"
			}
		],
		"name": "getSubaddressAndTokenids",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			},
			{
				"internalType": "uint256[][]",
				"name": "",
				"type": "uint256[][]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "subAddressList",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "subcontract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdrawETHEmergency",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_token",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_to",
				"type": "address"
			}
		],
		"name": "withdrawNFTs",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_token",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"internalType": "address[]",
				"name": "_subaddrs",
				"type": "address[]"
			},
			{
				"internalType": "uint256[][]",
				"name": "_tokenids",
				"type": "uint256[][]"
			}
		],
		"name": "withdrawNFTsV2",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
'''
contract = W3.eth.contract(address=W3.toChecksumAddress('0xED44409de91A340df26667E1FD21C9DA1EdE0Ef1'), abi=abi) # contract minter address

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

def deploy_subaddress():
    try:
        num = int(input("how many subaddress do you want to deploy? >>> "))
        nonce = W3.eth.getTransactionCount(MY_ADDR)
        params = {
            'from': MY_ADDR,
            'chainId': W3.toHex(W3.eth.chain_id),
            'value': W3.toHex(0),
            'nonce': W3.toHex(nonce)
        }
        ts = contract.functions.deploySubAddrs(num).buildTransaction(params)
        gas_price = ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']
        gas_limit = ts['gas']
        gas_cost = W3.fromWei(gas_price * gas_limit, 'ether')
        print(f"max gas cost: {round(gas_cost, 4)} ETH")
        ans = input("do you want to continue? (y/n) >>> ")
        if ans == 'y':
            W3.eth.call(ts)
            signed_txn = W3.eth.account.sign_transaction(ts, MY_PRIVATE_KEY)
            tx_hash = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"tx_hash: {tx_hash.hex()} , please wait for a while to get the receipt")
            receipt = W3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"deploy {num} subaddress success! cost {round(W3.fromWei(receipt['gasUsed'] * receipt['effectiveGasPrice'], 'ether'), 4)} ETH")
        else:
            print("abort")
    except Exception as e:
        print(e)

def show_subaddress():
    try:
        print("fetching your subaddress...")
        subaddrs = contract.functions.getSubaddress(MY_ADDR).call()
        for i, addr in enumerate(subaddrs[1]):
            print(f"{i+1}: {addr}")
    except Exception as e:
        print(e)

def mint_nfts():
    try:
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
            value = input("please input the price (not total price) >>> ")
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
        gas_price = ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']
        gas_limit = ts['gas']
        gas_cost = W3.fromWei(gas_price * gas_limit, 'ether')
        print(f"max gas cost: {round(gas_cost, 4)} ETH")
        ans = input("do you want to continue? (y/n) >>> ")
        if ans == 'y':
            W3.eth.call(ts)
            signed_txn = W3.eth.account.sign_transaction(ts, MY_PRIVATE_KEY)
            tx_hash = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"tx_hash: {tx_hash.hex()} , please wait for a while to get the receipt")
            receipt = W3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"mint NFTs success! cost {round(W3.fromWei(receipt['gasUsed'] * receipt['effectiveGasPrice'] , 'ether'), 4)} ETH")
        else:
            print("abort")

    except Exception as e:
        print(e)

def withdraw_nfts():
    try:
        nft_addr = W3.toChecksumAddress(input("please input the NFTs contract address >>> "))
        print("fetching your NFTs...")
        res = contract.functions.getSubaddressAndTokenids(MY_ADDR, nft_addr).call()
        subaddrs = res[0]
        tokenids = res[1]

        # [['0xE37AcFeFA707CBb55a359E0cF3e057666f29AD68', '0x0000000000000000000000000000000000000000', '0x0Ad087E122eF7fdd26dCdb487EF8820ceb323cb0'], [[], [], [7, 8, 26, 27, 28, 29, 30]]]
        # due to some logic errors in the contract code getSubaddressAndTokenids
        # sometimes the tokenids is empty and the subaddrs is wrong, so we need to filter it
        # if u have good solidity skills, please submit a PR to fix it
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
        gas_price = ts['maxFeePerGas'] + ts['maxPriorityFeePerGas']
        gas_limit = ts['gas']
        gas_cost = W3.fromWei(gas_price * gas_limit, 'ether')
        print(f"max gas cost: {round(gas_cost, 4)} ETH")
        ans = input("do you want to continue? (y/n) >>> ")
        if ans == 'y':
            W3.eth.call(ts)
            signed_txn = W3.eth.account.sign_transaction(ts, MY_PRIVATE_KEY)
            tx_hash = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"tx_hash: {tx_hash.hex()} , please wait for a while to get the receipt")
            receipt = W3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"withdraw NFTs success! cost {round(W3.fromWei(receipt['gasUsed'] * receipt['effectiveGasPrice'] , 'ether'), 4)} ETH")
        else:
            print("abort")
    except Exception as e:
        print(e)


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
        except:
            print('Invalid input')

if __name__ == "__main__":
    if W3.isConnected():
        main()
    else:
        print("web3 connection error, please check your provider")
