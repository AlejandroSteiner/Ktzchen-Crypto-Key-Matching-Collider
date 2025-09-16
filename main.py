import json
import logging
import os
import hashlib
import random
import ecdsa
from eth_account import Account
from web3 import Web3
import requests
import multiprocessing
import time
import tkinter as tk
from config import RPC_URL, NUM_CORES

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ethereum node connection
def connect_ethereum_node(using_infura, infura_url=None, infura_key=None):
    if using_infura:
        if infura_url and infura_key:
            return Web3(Web3.HTTPProvider(f"{infura_url}{infura_key}"))
        else:
            logging.error("Infura URL or API Key not provided")
            raise ValueError("Infura URL or API Key not provided")
    else:
        return Web3(Web3.HTTPProvider('http://localhost:8545'))

# Initialize global variable for Web3
w3 = None

def call_rpc(method, params=None, wallet_name=None):
    payload = {
        "method": method,
        "params": params or [],
        "jsonrpc": "1.0",
        "id": random.randint(1, 1000000),
    }
    headers = {'content-type': 'application/json'}
    wallet_path = f"/wallet/{wallet_name}" if wallet_name else ""
    response = requests.post(RPC_URL + wallet_path, data=json.dumps(payload), headers=headers)
    response_json = response.json()
    if 'error' in response_json and response_json['error'] is not None:
        logging.error(f"RPC Error: {response_json['error']}")
        return None
    return response_json['result']

def generate_bitcoin_address():
    try:
        new_address = call_rpc("getnewaddress", wallet_name="legacy_wallet")
        if new_address is None:
            raise ValueError("Bitcoin address was not generated correctly")
        
        private_key = call_rpc("dumpprivkey", [new_address], wallet_name="legacy_wallet")
        if private_key is None:
            raise ValueError("Private key was not retrieved correctly")
        
        return private_key, new_address
    except Exception as e:
        logging.error(f"Error in Bitcoin RPC connection: {str(e)}")
        return None, None

def load_addresses_from_file(file):
    try:
        with open(file, 'r') as f:
            addresses = f.read().splitlines()
        return addresses
    except Exception as e:
        logging.error(f"Error loading addresses from file: {str(e)}")
        return []

def generate_ethereum_private_key(bitcoin_address, identifier):
    private_key_hash = hashlib.sha256((bitcoin_address + str(identifier)).encode()).digest()
    eth_private_key = private_key_hash[:32]
    eth_private_key_ecdsa = ecdsa.SigningKey.from_string(eth_private_key, curve=ecdsa.SECP256k1)
    return eth_private_key_ecdsa

def get_ethereum_info(ethereum_address):
    try:
        balance = w3.eth.get_balance(ethereum_address)
        transactions = w3.eth.get_transaction_count(ethereum_address)
        return balance, transactions
    except Exception as e:
        logging.error(f"Error getting Ethereum info: {str(e)}")
        return None, None

def process_address(bitcoin_address_tuple):
    bitcoin_address, bitcoin_private_key, num_ethereum_keys = bitcoin_address_tuple

    # Verify that num_ethereum_keys is an integer
    if not isinstance(num_ethereum_keys, int):
        logging.error(f"The number of Ethereum keys ({num_ethereum_keys}) is not an integer.")
        return []

    logging.info(f"Processing Bitcoin address {bitcoin_address}...")

    results = []
    for i in range(num_ethereum_keys):
        logging.info(f" Generating private key {i + 1} of {num_ethereum_keys} for Bitcoin address {bitcoin_address}...")
        identifier = random.randint(1, 1000000)
        eth_private_key = generate_ethereum_private_key(bitcoin_address, identifier)
        eth_account = Account.from_key(eth_private_key.to_string().hex())
        eth_address = eth_account.address

        try:
            balance, transactions = get_ethereum_info(eth_address)
        except Exception as e:
            logging.error(f"Error getting Ethereum info: {str(e)}")
            continue

        result = {
            "bitcoin_address": bitcoin_address,
            "eth_private_key": eth_private_key.to_string().hex(),
            "eth_address": eth_address,
            "balance": balance,
            "transactions": transactions
        }
        results.append(result)

        logging.info(f"  - Processing Ethereum private key for Bitcoin address {bitcoin_address}: {eth_private_key.to_string().hex()}")
        logging.info(f"    - Ethereum public address: {eth_address}")

    return results

def main(num_bitcoin_addresses, num_ethereum_keys_per_address, num_cores, log_text=None, address_file=None, using_infura=False, infura_url=None, infura_key=None):
    global w3
    w3 = connect_ethereum_node(using_infura, infura_url, infura_key)

    # Verify that num_bitcoin_addresses and num_ethereum_keys_per_address are integers
    if isinstance(num_bitcoin_addresses, str):
        try:
            num_bitcoin_addresses = int(num_bitcoin_addresses)
        except ValueError:
            logging.error(f"The value of num_bitcoin_addresses ({num_bitcoin_addresses}) is not a valid integer.")
            return
    if isinstance(num_ethereum_keys_per_address, str):
        try:
            num_ethereum_keys_per_address = int(num_ethereum_keys_per_address)
        except ValueError:
            logging.error(f"The value of num_ethereum_keys_per_address ({num_ethereum_keys_per_address}) is not a valid integer.")
            return

    logging.info("Starting the address reading and conversion process...")
    if log_text:
        log_text.insert(tk.END, "Starting the address reading and conversion process...\n")
        log_text.see(tk.END)

    bitcoin_addresses = []

    if address_file:
        bitcoin_addresses = load_addresses_from_file(address_file)
        # Verify that each entry in bitcoin_addresses is a tuple with the third element as an integer
        for i, address in enumerate(bitcoin_addresses):
            if isinstance(address, str):
                bitcoin_addresses[i] = (address, "", num_ethereum_keys_per_address)
            elif isinstance(address, tuple) and len(address) == 3 and isinstance(address[2], int):
                continue
            else:
                logging.error(f"Invalid format in Bitcoin address: {address}")
                return
    else:
        for _ in range(num_bitcoin_addresses):
            bitcoin_private_key, bitcoin_public_key = generate_bitcoin_address()
            if bitcoin_private_key and bitcoin_public_key:
                logging.info(f"Bitcoin private key: {bitcoin_private_key}")
                logging.info(f"Bitcoin public address: {bitcoin_public_key}")
                bitcoin_addresses.append((str(bitcoin_public_key), str(bitcoin_private_key), num_ethereum_keys_per_address))
                if log_text:
                    log_text.insert(tk.END, f"Bitcoin private key: {bitcoin_private_key}\n")
                    log_text.insert(tk.END, f"Bitcoin public address: {bitcoin_public_key}\n")
            else:
                logging.error("Could not generate a Bitcoin address.")
                if log_text:
                    log_text.insert(tk.END, "Could not generate a Bitcoin address.\n")
                continue

    logging.info("Generating private keys and Ethereum addresses...")
    if log_text:
        log_text.insert(tk.END, "Generating private keys and Ethereum addresses...\n")
        log_text.see(tk.END)

    start_time = time.time()
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(process_address, bitcoin_addresses)
    end_time = time.time()

    logging.info(f"Processing time: {end_time - start_time} seconds")
    if log_text:
        log_text.insert(tk.END, f"Processing time: {end_time - start_time} seconds\n")
        log_text.see(tk.END)

    os.makedirs('data', exist_ok=True)

    logging.info("Saving results...")
    if log_text:
        log_text.insert(tk.END, "Saving results...\n")
        log_text.see(tk.END)

    return results

def verify_results(results):
    results_with_balance = []
    addresses_with_balance_found = False

    for result_list in results:
        for result in result_list:
            bitcoin_address = result["bitcoin_address"]
            ethereum_address = result["eth_address"]
            bitcoin_balance = verify_bitcoin_balance(bitcoin_address)
            ethereum_balance = verify_ethereum_balance(ethereum_address)
            if bitcoin_balance or ethereum_balance:
                addresses_with_balance_found = True
                results_with_balance.append(result)

    if addresses_with_balance_found:
        logging.info("Ethereum or Bitcoin addresses with balance found.")
        with open('data/results_with_balance.json', 'w') as f:
            json.dump(results_with_balance, f, indent=4)

        with open('data/results_with_balance.txt', 'w') as f:
            for result in results_with_balance:
                f.write(f"Bitcoin Address: {result['bitcoin_address']}\n")
                f.write(f"Private Key Bitcoin: {result['eth_private_key']}\n")
                f.write(f"Ethereum Address: {result['eth_address']}\n")
                f.write(f"Ethereum Balance: {result['balance']}\n")
                f.write(f"Ethereum Transactions: {result['transactions']}\n")
                f.write("\n")
    else:
        logging.info("No addresses with balance found.")
        
def verify_bitcoin_balance(address):
    try:
        balance = call_rpc("getreceivedbyaddress", [address])
        return balance
    except Exception as e:
        logging.error(f"Error verifying Bitcoin balance: {str(e)}")
        return None

def verify_ethereum_balance(address):
    try:
        balance = w3.eth.get_balance(address)
        return balance
    except Exception as e:
        logging.error(f"Error verifying Ethereum balance: {str(e)}")
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Coin matcher for Bitcoin and Ethereum.')
    parser.add_argument('num_bitcoin_addresses', type=int, help='Number of Bitcoin addresses to generate.')
    parser.add_argument('num_ethereum_keys_per_address', type=int, help='Number of Ethereum keys per Bitcoin address.')
    parser.add_argument('num_cores', type=int, help='Number of CPU cores to use.')
    parser.add_argument('--address_file', type=str, help='File with Bitcoin addresses to process.')
    parser.add_argument('--using_infura', action='store_true', help='Indicates whether to use Infura for connecting to Ethereum.')
    parser.add_argument('--infura_url', type=str, help='Infura URL.')
    parser.add_argument('--infura_key', type=str, help='Infura API Key.')

    args = parser.parse_args()

    results = main(args.num_bitcoin_addresses, args.num_ethereum_keys_per_address, args.num_cores, None, args.address_file, args.using_infura, args.infura_url, args.infura_key)
    verify_results(results)
























