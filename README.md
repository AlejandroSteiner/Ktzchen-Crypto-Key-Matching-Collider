# 🐾 Ktzchen - Crypto Key Matching Collider

**Ktzchen** It is a research tool in cryptography and blockchain that allows:
- 🔑 Generate **Bitcoin** public addresses and **Ethereum** private keys.  
- 🔗 Connect to your own **Bitcoin Core** and **Ethereum Geth** nodes, or use external services like **Ktzchen Web3**.  
- ⚡ Run processes in parallel (multi-core) to optimize performance.  
- 📊 Explore the relationship between keys and addresses, as part of educational and security testing.  

⚠️ **Note:** This software is for **educational and research pruposes**. It should not be used for illegal purposes or to compromise third-party funds.  

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
