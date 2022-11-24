#![allow(unused)]
// extern crate curl;

// use curl::easy::Easy;
use std::{io::{stdout, Write, Read}, any::{Any}};


use clap::{Parser, builder::Str};
use anyhow::{Context, Result};
use std::error::Error;
// use http::client::RequestWriter;
// use http::method::Get;
// use http::status;
use std::os;
use std::process;
use regex::Regex;
//use serde_json;
use serde_json::{Value,};
use reqwest::{blocking};
use futures::executor;
use web3::{
    ethabi::ethereum_types::U256,
    types::{Address, TransactionRequest,BlockId, BlockNumber, U64},
    api::Web3
};
use chrono::{DateTime, NaiveDate, NaiveDateTime, NaiveTime, Date};
use std::any::type_name;



/// ETH blockchain CLI explorer.
#[derive(Parser, Debug)]
struct Cli {
    /// The ETH address to examine
    #[arg(short, long)]
    address: String,

    /// Starting examining block
    #[arg(short, long)]
    block: Option<u64>,

}


fn type_of<T>(_: T) -> &'static str {
    type_name::<T>()
}

fn parse_date(date: &str) -> NaiveDateTime {
    let mut parsing_date = "00:00:00 ".to_owned();
    parsing_date.push_str(date);
    return NaiveDateTime::parse_from_str(&parsing_date, "%H:%M:%S %Y-%m-%d").unwrap();
}

#[tokio::main]
//async fn main() -> web3::Result<(), Box<dyn std::error::Error>> {
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // CLI check
    let args: Cli = Cli::parse();

    // ETH scan check
    // Check if provided wallet has some blocks
    let mut url: String = "https://api.etherscan.io/api?module=account&action=txlist&startblock=0&offset=10000&sort=asc&apikey=<ETH_SCAN_API_KEY>&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&address=".to_owned();

    let full_url: String = url + &args.address;
    let mut body = reqwest::get(&full_url)
        .await?.text().await?;

    let response: serde_json::Value = serde_json::from_str(&body)?;
    let status = response.get("status");
    let message = response.get("message");
    let blocks = response.get("result");

    if !status.unwrap().to_string().contains("1") || !message.unwrap().to_string().contains("OK")  {
        eprintln!("Given wallet is invalid or it has no block records");
        process::exit(1);
    }
    

    let transport = web3::transports::Http::new("https://mainnet.infura.io/v3/<INFURA_KEY>")?;
    let web3 = web3::Web3::new(transport);

    let mut accounts = web3.eth().accounts().await?;
    accounts.push(args.address.parse().unwrap());

    for account in accounts {
        let balance = web3.eth().balance(account, None).await?;
        println!("Current balance of {:?}: {}", account, balance);
    }

    for block in blocks.unwrap().as_array().unwrap() {
        // convert to proper types
        // block number string is enclosed in double quote marks
        // block number string to number(u64)
        // eth type conversion in order to get all transactions based on certain block number
        let block_num = block.get("blockNumber").unwrap().to_string().replace('"', "").parse::<u64>().unwrap();
        
        if args.block.is_some() {
            if args.block.unwrap() > block_num {
                // block number is provided to the CLI tool
                // skip this block since it is less then requested
                continue;
            }
        }

        let block_num_id = BlockId::Number(BlockNumber::Number((U64([block_num]))));
        let block_info = web3.eth().block_with_txs(block_num_id).await?.unwrap();
        let block_timestamp = i64::try_from(block_info.timestamp).ok().unwrap();


        
        println!("\nBlock: {:?}\nHash: {:?}", block_num, block_info.hash.unwrap());
        println!("Date: {:?}", NaiveDateTime::from_timestamp(block_timestamp, 0).to_string());
        for transaction in block_info.transactions {
            //println!("{:#?}", transaction);

            // more human-readable
            println!("Transaction {:?}:  https://ethplorer.io/tx/{:?} ", transaction.transaction_index.unwrap(), transaction.hash);
        }
        println!("\n\n\n\n");

    }

    Ok(())
}
