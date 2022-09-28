from blockchain import *
import pandas as PD
from hexbytes import (
    HexBytes,
)


if not isConnectedToETH():
    raise Exception(f"NOT CONNECTED TO BLOCKCHAIN NETWORK")

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
ST.set_page_config(page_title="ETH CRAWLER", page_icon=":computer:", layout="wide")

ST.header("ETH CRAWLER")
notificationBox: ST.container = ST.container()
with ST.form("wallet_form", True):
    walletInput: str       = ST.text_input("Wallet Address:", value="", key="wallet", placeholder="0x5fXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    blockInput:  Number    = ST.number_input("Starting block")
    dateInput:   DateValue = ST.date_input("Filter by date(2015-07-29 will be skipped)", key="date", min_value=Date(2015, 7, 29), max_value=Date.today(), value=Date(2015, 7, 29))
    formSubmit:  bool      = ST.form_submit_button("Check")
    data:        Any       = None
    if formSubmit:
        print(blockInput)
        notificationBox.empty()

        if walletInput is None or not isWalletAddressValid(walletInput.strip()):
            notificationBox.error(f"Invalid wallet provided {walletInput}!")
            ST.stop()

        if dateInput == Date(2015, 7, 29):
            # ETH released 2015-07-30
            # skip date filtering
            dateInput = None

        with ST.spinner(f"Loading for {walletInput}..."):
            data    = getFilteredTransactions(walletInput.strip(), blockInput, dateInput)
            balance = getBalance(walletInput.strip())
        
        if len(data) == 0:
            notificationBox.warning("No data found for given wallet!")
            ST.stop()
        
        #contentBox = ST.container()
        with ST.container():
            ST.subheader(f"Current wallet balance: {balance} ETH")
            for block in data:
                with ST.expander(f"Block: {block.number}\n {block.hash.hex()}"):
                    tabOverview, tabTxs = ST.tabs(["Overview", "Transactions"])
                    with tabOverview:
                        ST.caption(f"Block number: {block.number}")
                        ST.caption(f"Block size: {block.size}")
                        ST.caption(f"Block hash: {block.hash.hex()}")
                        ST.caption(f"Mix hash: {block.mixHash.hex()}")
                        if "miner" in block:
                            ST.caption(f"Miner: {block.miner}")
                        if "parentHash" in block:
                            ST.caption(f"Parent hash: {block.parentHash.hex()}")
                        ST.caption(f"Gas limit: {convertUnit(block.gasLimit)} ETH")
                        ST.caption(f"Gas used: {convertUnit(block.gasUsed)} ETH")
                        ST.caption(f"UTC Time: {Datetime.utcfromtimestamp(block.timestamp)}")
                        if "nonce" in block:
                            ST.caption(f"Nonce: {block.nonce.hex()}")
                        if "receiptRoot" in block:
                            ST.caption(f"Receipt Root: {block.receiptRoot.hex()}")
                        if "stateRoot" in block:
                            ST.caption(f"Stete root: {block.stateRoot.hex()}")
                        if "difficulty" in block:
                            ST.caption(f"Difficulty: {block.difficulty}")
                        if "totalDifficulty" in block:
                            ST.caption(f"Total Difficulty: {block.totalDifficulty}")
                        if "sha3Uncles" in block:
                            ST.caption(f"Sha3Uncles: {block.sha3Uncles.hex()}")
                        if "uncles" in block:
                            ST.caption(f"Uncles: {block.uncles}")
                        if "logsBloom" in block:
                            ST.caption(f"Logs Bloom: {block.logsBloom.hex()}")
                        if "extraData" in block:
                            ST.caption(f"Extra Data: {block.extraData.hex()}")
                        if "transactionsRoot" in block:
                            ST.caption(f"Transactions Root: {block.transactionsRoot.hex()}")
                    
                    with tabTxs:
                        if len(block.transactions) == 0:
                            ST.header("No transactions found.")
                            ST.stop()
                        
                        columns = ["accessList", "blockHash", "blockNumber", "chainId", "data", "from", "gas", "gasPrice", "maxFeePerGas", "maxPriorityFeePerGas", "hash", "input", "nonce", "r", "s", "to", "transactionIndex", "type", "v", "value"]
                        txsData = []

                        for tx in block.transactions:
                            temp = [
                                str(tx.get("accessList", [])),
                                str(tx.get("blockHash", HexBytes("")).hex()),
                                str(tx.get("blockNumber", 0)),
                                str(tx.get("chainId", "/")),
                                str(tx.get("data", HexBytes("")).hex()),
                                str(tx.get("from", "/")),
                                str(tx.get("gas", 0)),
                                str(tx.get("gasPrice", 0)),
                                str(tx.get("maxFeePerGas", 0)),
                                str(tx.get("maxPriorityFeePerGas", 0)),
                                str(tx.get("hash", HexBytes("")).hex()),
                                str(tx.get("input", "/")),
                                str(tx.get("nonce", 0)),
                                str(tx.get("r", HexBytes("")).hex()),
                                str(tx.get("s", HexBytes("")).hex()),
                                str(tx.get("to", "/")),
                                str(tx.get("transactionIndex", 0)),
                                str(tx.get("type", 0)),
                                str(tx.get("v", 0)),
                                str(tx.get("value", 0))
                            ]
                            txsData.append(temp)
                                                
                        ST.dataframe(PD.DataFrame(txsData,columns=columns))



