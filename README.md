# 🐾 Ktzchen - Crypto Key Matching Collider

**Ktzchen** It is a research tool in cryptography and blockchain that allows:
- 🔑 Generate **Bitcoin** public addresses and **Ethereum** private keys.  
- 🔗 Connect to your own **Bitcoin Core** and **Ethereum Geth** nodes, or use external services like **Ktzchen Web3**.  
- ⚡ Run processes in parallel (multi-core) to optimize performance.  
- 📊 Explore the relationship between keys and addresses, as part of educational and security testing.  

⚠️ **Note:** This software is for **educational and research pruposes**. It should not be used for illegal purposes or to compromise third-party funds. 


📝 Technical Description 

Ktzchen - Crypto Key Matching Collider is a cryptographic research tool for exploring Bitcoin and Ethereum key spaces, with detailed matching and balance checking.

The software works as follows:

Generate Bitcoin addresses

The program generates Bitcoin public addresses based on the configured parameters.

Check Bitcoin balances

For each generated or loaded Bitcoin address, it queries the node or API to check if the address has a balance.

If the address has a positive balance, the software prints:

The Bitcoin address

The corresponding private key

The balance

Generate Ethereum private keys

For each Bitcoin address (or for each batch), the software generates one or multiple Ethereum private keys.

Check Ethereum balances

Each generated Ethereum private key is converted into its corresponding public address.

The software queries the Ethereum node or API to check if there is any balance.

If a balance is found, it prints:

The Ethereum address

The private key

The balance

Modes of operation

Own Nodes Mode: Directly queries your local Bitcoin Core node (RPC) and Ethereum Geth node (HTTP).

File + API Key Mode: Uses a .txt file of Bitcoin addresses and an API key from a service like ktzchenweb3.io.

Parallel execution (multi-core)

The software can run multiple address/key checks in parallel to speed up the process.

Logging and results

All addresses with balances are printed in the console/log.

The tool can be used to study key space, balance distribution, and potential overlaps for research purposes.
 

## 🚀 Installation

```bash
git clone https://github.com/AlejandroSteiner/Ktzchen-Crypto-Key-Matching-Collider.git
cd Ktzchen-Crypto-Key-Matching-Collider
pip install -r requirements.txt
```

Run the graphical interface:

```bash
python gui.py
```



⚙️ How to Use

1. Launch the GUI

```bash
python gui.py
```

2. Choose the connection mode

.Own Nodes Mode

   .Connect to your Bitcoin Core node (RPC enabled).

   .Connect to your Ethereum (Geth) node (HTTP enabled).

.File + API Key Mode

   .Load a .txt file with Bitcoin addresses (one per line).

   .Enter your API key from a service like ktzchenweb3.io

3.Configure parameters in the interface

   .Number of Bitcoin addresses to process.

   .Number of Ethereum keys to generate per address.

   .Number of CPU cores to use.

4.Start the process

   .Click Start in the interface.

  .Logs and progress will appear in real-time on the console area.
  

📂 Example Setup with File + API Key

.File addresses.txt:

```text
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
bc1qw508d6qejxtdg4y5r3zarvary0c5xw7k3g4ty
```
.API Key example:

```text
https://api.ktzchenweb3.io/v1/mainnet
YOUR_API_KEY
```
Load the file and API key through the GUI, then run the process ✅.


🖥️ Requirements

.Python 3.10+

.Optional nodes:

   .Bitcoin Core (if using own node mode)

   .Geth (if using own node mode)

.Dependencies listed in requirements.txt
