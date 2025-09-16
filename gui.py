import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from main import main
import logging
import configparser

class KtzchenCryptoKeyMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ktzchen - Crypto Key Matching Software")
        self.root.geometry("750x750")  # Window size adjustment
        self.create_widgets()

    def create_widgets(self):
        # Frame for node configuration
        self.frame_node = tk.LabelFrame(self.root, text="Node Configuration", padx=10, pady=10)
        self.frame_node.pack(fill="x", padx=10, pady=5)

        self.radio_var = tk.IntVar(value=1)

        self.radio_own_node = tk.Radiobutton(self.frame_node, text="Use Own Bitcoin Node and Web3 Node", variable=self.radio_var, value=1, command=self.toggle_options)
        self.radio_own_node.grid(row=0, column=0, sticky="w")

        self.radio_load_file = tk.Radiobutton(self.frame_node, text="Load Addresses from File", variable=self.radio_var, value=2, command=self.toggle_options)
        self.radio_load_file.grid(row=1, column=0, sticky="w")

        self.label_file = tk.Label(self.frame_node, text="Address File:")
        self.label_file.grid(row=2, column=0, sticky="e")

        self.entry_file = tk.Entry(self.frame_node, state="disabled", width=40)
        self.entry_file.grid(row=2, column=1, pady=5)

        self.button_load_file = tk.Button(self.frame_node, text="Load", command=self.load_file, state="disabled")
        self.button_load_file.grid(row=2, column=2, padx=5)

        # Frame for input configurations
        self.frame_config = tk.LabelFrame(self.root, text="CPU - MEMORY RAM Configurations", padx=10, pady=10)
        self.frame_config.pack(fill="x", padx=10, pady=5)

        tk.Label(self.frame_config, text="Number of Bitcoin Addresses:").grid(row=0, column=0, sticky="w")
        self.num_addresses = tk.Entry(self.frame_config)
        self.num_addresses.grid(row=0, column=1)

        tk.Label(self.frame_config, text="Number of Ethereum Keys per Address:").grid(row=1, column=0, sticky="w")
        self.num_keys = tk.Entry(self.frame_config)
        self.num_keys.grid(row=1, column=1)

        tk.Label(self.frame_config, text="Number of CPU Cores:").grid(row=2, column=0, sticky="w")
        self.num_cores = tk.Entry(self.frame_config)
        self.num_cores.grid(row=2, column=1)

        # Web3 Configuration
        self.frame_infura = tk.LabelFrame(self.root, text="Web3 Configuration", padx=10, pady=10)
        self.frame_infura.pack(fill="x", padx=10, pady=5)
        
        self.label_infura_url = tk.Label(self.frame_infura, text="Web3 URL:")
        self.label_infura_url.grid(row=0, column=0, sticky="e")
        
        self.entry_infura_url = tk.Entry(self.frame_infura, state="disabled", width=40)
        self.entry_infura_url.grid(row=0, column=1, pady=5)
        
        self.label_infura_key = tk.Label(self.frame_infura, text="Web3 API Key:")
        self.label_infura_key.grid(row=1, column=0, sticky="e")
        
        self.entry_infura_key = tk.Entry(self.frame_infura, state="disabled", width=40)
        self.entry_infura_key.grid(row=1, column=1, pady=5)

        # Frame for log and process start
        self.frame_log = tk.LabelFrame(self.root, text="Process Log", padx=10, pady=10)
        self.frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = ScrolledText(self.frame_log, height=10, bg="#561244", fg="white")
        self.log_text.pack(fill="both", expand=True)

        # Button to start the process
        self.button_start = tk.Button(self.root, text="Start Process", command=self.start_process)
        self.button_start.pack(pady=10)

        # Footer
        self.label_footer = tk.Label(self.root, text="Ktzchen - Crypto Key Matching Software v1.0 2024", font=("Helvetica", 8))
        self.label_footer.pack(side="bottom")

    def toggle_options(self):
        if self.radio_var.get() == 1:
            self.entry_file.config(state="disabled")
            self.button_load_file.config(state="disabled")
            self.num_addresses.config(state="normal")
            self.entry_infura_url.config(state="disabled")
            self.entry_infura_key.config(state="disabled")
        else:
            self.entry_file.config(state="normal")
            self.button_load_file.config(state="normal")
            self.num_addresses.config(state="disabled")
            self.entry_infura_url.config(state="normal")
            self.entry_infura_key.config(state="normal")

    def load_file(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file)

    def start_process(self):
        num_addresses = self.num_addresses.get()
        num_keys = self.num_keys.get()
        num_cores = self.num_cores.get()
        address_file = self.entry_file.get() if self.radio_var.get() == 2 else None
        infura_url = self.entry_infura_url.get() if self.radio_var.get() == 2 else None
        infura_key = self.entry_infura_key.get() if self.radio_var.get() == 2 else None

        if self.radio_var.get() == 1 and not num_addresses:
            messagebox.showerror("Error", "You must specify the number of Bitcoin addresses.")
            return

        if not num_keys:
            messagebox.showerror("Error", "You must specify the number of Ethereum keys per address.")
            return

        if not num_cores:
            messagebox.showerror("Error", "You must specify the number of CPU cores.")
            return

        try:
            num_addresses = int(num_addresses) if num_addresses else 0
            num_keys = int(num_keys)
            num_cores = int(num_cores)
        except ValueError:
            messagebox.showerror("Error", "All fields must be integers.")
            return

        using_infura = self.radio_var.get() == 2  # If loading from file is selected, use Infura

        self.log_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_main, args=(num_addresses, num_keys, num_cores, address_file, using_infura, infura_url, infura_key)).start()

    def run_main(self, num_addresses, num_keys, num_cores, address_file, using_infura, infura_url, infura_key):
        try:
            results = main(num_addresses, num_keys, num_cores, self.log_text, address_file, using_infura, infura_url, infura_key)
            if results:
                messagebox.showinfo("Process Completed", "The process has successfully completed.")
            else:
                messagebox.showwarning("Warning", "The process completed, but no addresses with balance were found.")
        except Exception as e:
            logging.error(f"Error running the process: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KtzchenCryptoKeyMatcherApp(root)
    root.mainloop()



































