# Ethereum transactions crawler task

Dear **OriginTrail**, I wanted to say BIG thank you for this opportunity, I saw and learned some great stuff while working on this task.

In desire to express myself on how much I want to work for with you, I was able to make 2 small apps for this task. GUI based one is written in Python and second one is CLI based written in Rust. On your website I saw that you are working with Rust so I hope you don't mind me challenging myself in order to try doing this task in Rust also.


## Python GUI-based app

This is server-rendered app, located in *python* folder and there are multiple ways of running it in your local environment:
1. **Docker**

In your terminal/console, navigate to python folder and create docker image:
```
docker build -t eth-crawler . 
```
When docker image is created, run it in isolated container environment with command:
```
docker run -p 5000:5000 eth-crawler
```
In your browser, open http://0.0.0.0:5000/app URL



2. **Install Python interpreter and its tools locally**

Visit page https://www.python.org/downloads/ and follow the installation instructions

Install Python package installer, follow the instruction page https://pip.pypa.io/en/stable/installation/#get-pip-py 

[Optional] You can also install virtual environment to isolate environment: https://virtualenv.pypa.io/en/latest/installation.html#via-pip

Once everything is installed, in your terminal/console, navigate to python folder of this project and run:
```
pip3 install -r requirements.txt
```
Above command downloads required modules and next is to run the app:
```
streamlit run app.py --server.runOnSave=true --server.address=0.0.0.0 --server.port=5000 --server.baseUrlPath=/app --server.enableCORS=true --ui.hideTopBar=true --ui.hideSidebarNav=true --theme.base=dark
```
In your browser, open http://0.0.0.0:5000/app URL





GUI tool has simple and clean UI. By providing ETH wallet, there are options to see all blocks and their transactions and also you can filter by date and starting blocks.




## Rust CLI-based app

Based on your OS, follow instructions on how to install Rust locally: https://www.rust-lang.org/tools/install

After rust installation and  cloning this repository to your local machine, navigate to rust/ethereum_crawler folder and build the project with command:
```
cargo build
```
After building is successful, target/debug folder is created, you can run created binary by running:
```
target/debug/ethereum_crawler --address 0xXXXXXXXXXXXXXXXXXX
```
or
```
cd target/debug/ && ./ethereum_crawler --address 0xXXXXXXXXXXXXXXXXXX
```


Due to my private obligations and my current job, I was not able to add filtering blocks by given date, however CLI tool has option to filter by starting block:
```
target/debug/ethereum_crawler --address 0xXXXXXXXXXXXXXXXX -b 14234234
```
also listing of all CLI options:
```
target/debug/ethereum_crawler --help                                                          
ETH blockchain CLI explorer

Usage: ethereum_crawler [OPTIONS] --address <ADDRESS>

Options:
  -a, --address <ADDRESS>  The ETH address to examine
  -b, --block <BLOCK>      Starting examining block
  -h, --help               Print help information
```                                                                                                                                                                  
If you want for CLI tool to absolutely print all transaction data(not very human readable), uncomment line 118 in **src/main.rs** file and build code again.
















