from web3 import Web3
from web3.types import BlockData
import requests as Requests
import time as Time
import sys as Sys
from datetime import datetime as Datetime, date as Date
import os as OS
from typing_extensions import TypeAlias
from typing import Union, Any
import streamlit as ST


ETHSCAN:   str       = "ETHSCAN_KEY"
INFURA:    str       = "INFURA_KEY"
DateValue: TypeAlias = Union[Date, Datetime, None]
Number:    TypeAlias = Union[int, float]



def getWeb3() -> Web3:
    """Initialize Web3 object."""
    # Making connection with infura url for collecting ETH transactions
    infuraUrl: str = f"https://mainnet.infura.io/v3/{INFURA}"
    return Web3(Web3.HTTPProvider(infuraUrl))


def isConnectedToETH() -> bool:
    """Check if connection to ETH blockchain is established."""
    w3: Web3 = getWeb3()
    return w3.isConnected()


def isWalletAddressValid(ethAddress: str) -> bool:
    """Check if provided addresss is valid."""
    w3: Web3 = getWeb3()
    return w3.isAddress(ethAddress)


def getLatestBlockNumber() -> int:
    """Get latest processed block on ETH blockchain."""
    w3: Web3 = getWeb3()
    return w3.eth.block_number


def convertUnit(amount: int, unit: str="ether") -> float:
    """Convert unit."""
    units: str  = "wei/kwei/babbage/femtoether/mwei/lovelace/picoether/gwei/shannon/nanoether/nano/szabo/microether/micro/finney/milliether/milli/ether/kether/grand/mether/gether/tether"
    if unit not in units:
        #raise Exception(f"INVALID UNIT PROVIDED: {currencyUnit}")
        print(f"INVALID UNIT PROVIDED: {unit}")
        return -1
    return float(Web3.fromWei(amount, unit))


def getBalance(ethAddress: str, currencyUnit: str="ether") -> float:
    """Get balance based on given address."""
    units: str  = "wei/kwei/babbage/femtoether/mwei/lovelace/picoether/gwei/shannon/nanoether/nano/szabo/microether/micro/finney/milliether/milli/ether/kether/grand/mether/gether/tether"
    w3:    Web3 = getWeb3()
    if not w3.isAddress(ethAddress):
        #raise Exception(f"INVALID ETH ADDRESS PROVIDED: {ethAddress}")
        print(f"INVALID ETH ADDRESS PROVIDED: {ethAddress}")
        return -1
    
    if currencyUnit not in units:
        #raise Exception(f"INVALID UNIT PROVIDED: {currencyUnit}")
        print(f"INVALID UNIT PROVIDED: {currencyUnit}")
        return -1

    if not w3.isChecksumAddress(ethAddress):
        ethAddress = w3.toChecksumAddress(ethAddress)

    balance = w3.eth.get_balance(ethAddress)

    return float(w3.fromWei(balance, currencyUnit))


def getAllTransactions(ethAddress: str) -> list:
    """Get all transactions for given ETH address."""
    
    w3: Web3 = getWeb3()
    if not w3.isAddress(ethAddress):
        #raise Exception(f"INVALID ETH ADDRESS PROVIDED: {ethAddress}")
        print(f"INVALID ETH ADDRESS PROVIDED: {ethAddress}")
        return []

    ethScanUrl: str = f"https://api.etherscan.io/api?module=account&action=txlist&startblock=0&offset=10000&sort=asc&apikey={ETHSCAN}&address={ethAddress}"

    try:
        Time.sleep(1) # 5 limit per second may be reached
        response: Requests.Response = Requests.get(ethScanUrl)
        if response.status_code != 200:
            raise Exception(f"INVALID HTTP RESPONSE({response.status_code})")
        
        data: Any = response.json()

        if type(data) is not dict:
            raise Exception(f"[1]API ERROR - INVALID DATA TYPE: {type(data)}")

        if data.get("message", "~OK") != "OK" and data.get("status", -1) != 1:
            raise Exception(f"[2]API ERROR: {data}")
        
        return data.get("result")

    except Exception as e:
        print("HTTP ERROR: ", e)
        return []

@ST.cache()
def getFilteredTransactions(ethAddress: str, startBlock: int=0, filteredDate: DateValue=None) -> list:
    """Get all transactions based on given filters."""
    try:
        w3:           Web3 = getWeb3()
        transactions: list = []
        
        if not w3.isAddress(ethAddress):
            #raise Exception(f"INVALID ETH ADDRESS PROVIDED: {ethAddress}")
            print(f"INVALID ETH ADDRESS PROVIDED: {ethAddress}")
            return transactions
        
        ethScanUrl: str = f"https://api.etherscan.io/api?module=account&action=txlist&startblock=0&offset=10000&sort=asc&apikey={ETHSCAN}&address={ethAddress}"

        Time.sleep(1) # 5 limit per second may be reached
        response = Requests.get(ethScanUrl)
        if response.status_code != 200:
            raise Exception(f"INVALID HTTP RESPONSE({response.status_code})")
        
        returnData = response.json()
        
        if returnData.get("message", "~OK") != "OK" and returnData.get("status", -1) != 1:
            raise Exception(f"[1]API ERROR: {returnData}")
        
        for block in returnData.get("result", []):
            if type(block) is not dict:
                raise Exception(f"[2]API ERROR: INVALID DATA RESULTS: {block}")
            
            blockNum: int = int(block.get("blockNumber"))

            if startBlock > blockNum:
                # only blocks that are higher then start block are allowed
                continue
            
            loopBlock: BlockData = w3.eth.get_block(blockNum, full_transactions=True)
            blockTime: DateValue = Datetime.utcfromtimestamp(loopBlock.timestamp)

            if filteredDate is not None:
                if blockTime.date() != filteredDate:
                    # block not created on same day
                    continue

            transactions.append(loopBlock)

        return transactions

    except:
        _, _, excTb = Sys.exc_info()
        print(f"FAILED TO GET TRANSACTIONS DUE TO :: {str(Sys.exc_info())} ::: file: " + OS.path.abspath(excTb.tb_frame.f_code.co_filename) + " line:" + str(excTb.tb_lineno))
        return []


