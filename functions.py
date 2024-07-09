import json
import sqlite3
from web3 import Web3
from tkinter import *
import mysql.connector
from eth_keys import keys
from eth_utils import decode_hex
ganache_url = "HTTP://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))

owner_address = web3.eth.accounts[0]
owner_private_key = "0xb4a4b483ff6e509976e25def1104554d721a0c3a0dad902d8ba269e7b06f52ff"
web3.eth.default_account = web3.eth.accounts[0]
address = web3.to_checksum_address("0x5EbfC7b9505997feCA0e1798F47A00f57F73112f")
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"value","type":"uint256"}],"name":"ReturnValue","type":"event"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"addJourno","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"st","type":"address"},{"internalType":"uint256","name":"time","type":"uint256"},{"internalType":"string","name":"link","type":"string"},{"internalType":"uint256","name":"t","type":"uint256"}],"name":"addNews","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"block_list","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"link","type":"string"},{"internalType":"int256","name":"vote","type":"int256"}],"name":"castVote","outputs":[{"internalType":"uint256","name":"u","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"link","type":"string"},{"internalType":"int256","name":"vote","type":"int256"}],"name":"castVoteU","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"},{"internalType":"uint256","name":"new_rating","type":"uint256"}],"name":"changeRating","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"link","type":"string"}],"name":"checkNews","outputs":[{"components":[{"internalType":"address","name":"publisher","type":"address"},{"internalType":"uint256","name":"time","type":"uint256"},{"internalType":"enum Check.status","name":"s","type":"uint8"},{"internalType":"string","name":"link","type":"string"},{"internalType":"uint256","name":"t","type":"uint256"}],"internalType":"struct Check.News","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"decRating10","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"decRating20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"link","type":"string"}],"name":"findPublisher","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"getBlockCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"getRating","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"link","type":"string"}],"name":"getVotes","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"},{"internalType":"uint256","name":"change","type":"uint256"}],"name":"incRating","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"link","type":"string"}],"name":"isActive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"last20Links","outputs":[{"internalType":"string[20]","name":"ans","type":"string[20]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lastLinks","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"pending","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"rating","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"removeJourno","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"storeStatus","outputs":[{"internalType":"address","name":"publisher","type":"address"},{"internalType":"uint256","name":"time","type":"uint256"},{"internalType":"enum Check.status","name":"s","type":"uint8"},{"internalType":"string","name":"link","type":"string"},{"internalType":"uint256","name":"t","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"storeVotes","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}]')
contract = web3.eth.contract(address=address, abi = abi)
# current_address = web3.eth.accounts[0]
class Member():
    def pay_owner(amt, address, private_key):
            nonce = web3.eth._get_transaction_count(address)
            # amt = 0.25 * vote_val
            tx = {
                "from" : address,
                "nonce" : nonce,
                "to" : owner_address, 
                "value" : web3.to_wei(amt, 'ether'), 
                "gas" : 2000000, 
                "gasPrice" : web3.to_wei('50', 'gwei')
            }
            # privatek = "0x226263f4492fff3ff5055173a8ab1c9804bb0daf929ae92de529ddd27dc51c2c"
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    def register_payfees(address, private_key):
            web3.eth.default_account = web3.eth.accounts[0]
            amt = 1.5**contract.functions.getBlockCount(address).call()
            if web3.from_wei(web3.eth.get_balance(address), 'ether') >= amt:
                Member.pay_owner(amt, address, private_key)
                contract.functions.addJourno(address).transact()
                return 1
            else :
                return 0
    
    def login(address, private_key):
        try:
            pkb = decode_hex(private_key)
        except:
            return 0
        pk = keys.PrivateKey(pkb)
        puk = pk.public_key
        if address==puk.to_checksum_address():
            if contract.functions.getRating(address).call() == 0:
                return 2
            else :
                current_address = address
                return 1
        else : 
            return 0
        
    def publishU_payfees(address, private_key):
            web3.eth.default_account = web3.eth.accounts[0]
            amt = 1
            if web3.from_wei(web3.eth.get_balance(address), 'ether') >= amt:
                Member.pay_owner(amt, address, private_key)
                return 1
            else :
                return 0
       
    def publishS_payfees(address, private_key):
            web3.eth.default_account = web3.eth.accounts[0]
            amt = 2
            if web3.from_wei(web3.eth.get_balance(address), 'ether') >= amt:
                Member.pay_owner(amt, address, private_key)
                contract.functions.addJourno(address).transact()
                return 1
            else :
                return 0
        
    def factor_vote(address, publisher):
        conn = sqlite3.connect('registration_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT locX, locY FROM registrations WHERE address=?", (address,))
        addressxy = cursor.fetchone()
        address_y = addressxy[1]
        address_x = addressxy[0]
        cursor.execute("SELECT locX, locY FROM registrations WHERE address=?", (publisher,))
        publisherxy = cursor.fetchone()
        publisher_y = publisherxy[1]
        publisher_x = publisherxy[0]

        conn.close()
        val = pow(abs(address_x - publisher_x)**2 + abs(address_y - publisher_y)**2, 0.5)
        if val <= 1 :  return 5
        elif val <= 5 : return 4
        elif val <= 10 : return 3
        elif val <= 50 : return 2
        else : return 1
        
    def findPublisher(link):
        publisher = contract.functions.findPublisher(link).call()
        return publisher
    
    def viewNews(link):
        news = contract.functions.checkNews(link).call()
        return news
    
    def voteT(link, address, private_key):
        current_address = address
        vote_val = Member.factor_vote(current_address, Member.findPublisher(link))
        amt = 0.25 * vote_val
        if(amt > web3.from_wei(web3.eth.get_balance(web3.eth.default_account), 'ether')) : 
            return -1,-1
        else :
            out = contract.functions.castVote(link, vote_val).transact()
            event_filter = contract.events.ReturnValue.create_filter(fromBlock = "latest", toBlock = "latest")
            event_logs = event_filter.get_all_entries()
            if event_logs:
                returned_value = event_logs[0]['args']['value']
                out = returned_value
            else :
                out = -5
            nonce = web3.eth._get_transaction_count(current_address)
            tx = {
                "nonce" : nonce,
                "to" : owner_address, 
                "value" : web3.to_wei(0.25*vote_val, 'ether'), 
                "gas" : 2000000, 
                "gasPrice" : web3.to_wei('50', 'gwei')
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return out, amt 
        
    def voteF(link, address, private_key):
        current_address = address
        vote_val = Member.factor_vote(current_address, Member.findPublisher(link))
        amt = 0.25 * vote_val
        if(amt > web3.from_wei(web3.eth.get_balance(web3.eth.default_account), 'ether')) : 
            return -1, -1
        else :
            owner_address = web3.eth.accounts[0]
            out = contract.functions.castVote(link, 0 - vote_val).transact()
            event_filter = contract.events.ReturnValue.create_filter(fromBlock = "latest", toBlock = "latest")
            event_logs = event_filter.get_all_entries()
            if event_logs:
                returned_value = event_logs[0]['args']['value']
                out = returned_value
            else :
                out = -5
            nonce = web3.eth._get_transaction_count(current_address)
            tx = {
                "nonce" : nonce,
                "to" : owner_address, 
                "value" : web3.to_wei(0.25*vote_val, 'ether'), 
                "gas" : 2000000, 
                "gasPrice" : web3.to_wei('50', 'gwei')
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return out, amt
    
    def getRating(address):
        return contract.functions.getRating(address).call()
    
    def getLast20():
        return contract.functions.last20Links().call()
    
    def publishNewsS(address, link, time, private_key):
        web3.eth.default_account = web3.eth.accounts[0]
        current_address = address
        if(2 > web3.from_wei(web3.eth.get_balance(current_address), 'ether')):
            return 0
        else :
            current_address = address
            out = contract.functions.addNews(current_address, time, link, 0).transact()
            nonce = web3.eth._get_transaction_count(current_address)
            tx = {
                "nonce" : nonce,
                "to" : owner_address, 
                "value" : web3.to_wei(2, 'ether'), 
                "gas" : 2000000, 
                "gasPrice" : web3.to_wei('50', 'gwei')
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return out
    
    def publishNewsU(address, link, time, private_key):
        web3.eth.default_account = web3.eth.accounts[0]
        if(1 > web3.from_wei(web3.eth.get_balance(web3.eth.default_account), 'ether')):
            return 0
        else :
            current_address = address
            owner_address = web3.eth.accounts[0]
            out = contract.functions.addNews(current_address, time, link, 1).transact()
            nonce = web3.eth._get_transaction_count(current_address)
            tx = {
                "nonce" : nonce,
                "to" : owner_address, 
                "value" : web3.to_wei(1, 'ether'), 
                "gas" : 2000000, 
                "gasPrice" : web3.to_wei('50', 'gwei')
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return out
    
    def changeRating(address, new_rating):
        contract.functions.changeRating(address, new_rating).transact()
    
    def pay_from_owner(address, amt):
        nonce = web3.eth._get_transaction_count(web3.eth.accounts[0])
        tx = {
            "nonce" : nonce,
            "to" : address, 
            "value" : web3.to_wei(amt, 'ether'), 
            "gas" : 2000000, 
            "gasPrice" : web3.to_wei('50','gwei')
        }
        signed_tx = web3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        

    def getLast20():
        arr = contract.functions.last20Links().call()
        return arr
    
    def isActive(link):
        act = contract.functions.isActive(link).call()
        return act