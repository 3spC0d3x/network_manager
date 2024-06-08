import tkinter as tk
from tkinter import ttk, simpledialog
import psutil

class NetworkManager:
    def __init__(self):
        self.networks = {'Home': '192.168.1.1', 'Work': '10.0.0.1'}
        self.current_network = None
        self.current_dns = '8.8.8.8'  # DNS predeterminado

    def change_network(self, network_name):
        if network_name in self.networks:
            self.current_network = self.networks[network_name]
            print(f'Connected to {network_name} - IP: {self.current_network}')
        else:
            print(f'Error: {network_name} network not found!')

    def add_network(self, network_name, ip_address):
        self.networks[network_name] = ip_address
        print(f'Network {network_name} added with IP {ip_address}')

    def configure_network_usage(self):
        print("Configuring network usage...")
        # Aquí iría la lógica real para configurar el uso de la red

    def change_dns(self, new_dns):
        self.current_dns = new_dns
        print(f'DNS changed to {new_dns}')

    def get_network_usage(self):
        network_usage = psutil.net_io_counters()
        return f"Bytes sent: {network_usage.bytes_sent}, Bytes received: {network_usage.bytes_recv}"

class NetworkGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Network Manager")
        self.root.geometry("600x400")

        # Fuente y estilo
        self.custom_font = ("Consolas", 12)

        # Título
        self.title_label = ttk.Label(self.root, text="Select a Network", font=self.custom_font)
        self.title_label.pack()

        # Lista desplegable
        self.network_var = tk.StringVar()
        self.network_var.set("Select Network")
        self.network_dropdown = ttk.Combobox(self.root, textvariable=self.network_var, values=list(self.manager.networks.keys()), font=self.custom_font)
        self.network_dropdown.pack()

        # Botones
        self.change_button = ttk.Button(self.root, text="Change Network", command=self.change_network, style="Bold.TButton")
        self.change_button.pack()
        self.add_button = ttk.Button(self.root, text="Add Network", command=self.add_network, style="Bold.TButton")
        self.add_button.pack()

        # Menú de opciones
        self.menu_label = ttk.Label(self.root, text="Other Options", font=self.custom_font)
        self.menu_label.pack()

        self.option1_button = ttk.Button(self.root, text="Network Usage", command=self.show_network_usage, style="Bold.TButton")
        self.option1_button.pack()

        self.option2_button = ttk.Button(self.root, text="Change DNS", command=self.change_dns_dialog, style="Bold.TButton")
        self.option2_button.pack()

        # Etiqueta para mostrar el uso de la red
        self.network_usage_label = ttk.Label(self.root, text="", font=self.custom_font)
        self.network_usage_label.pack()

        # Iniciar GUI
        self.update_network_usage()
        self.root.mainloop()

    def change_network(self):
        network_name = self.network_var.get()
        self.manager.change_network(network_name)

    def add_network(self):
        network_name = simpledialog.askstring("Add Network", "Enter network name:")
        ip_address = simpledialog.askstring("Add Network", "Enter IP address:")
        if network_name and ip_address:
            self.manager.add_network(network_name, ip_address)

    def change_dns_dialog(self):
        new_dns = simpledialog.askstring("Change DNS", "Enter new DNS address:")
        if new_dns:
            self.manager.change_dns(new_dns)

    def show_network_usage(self):
        network_usage = self.manager.get_network_usage()
        self.network_usage_label.config(text=network_usage)

    def update_network_usage(self):
        network_usage = self.manager.get_network_usage()
        self.network_usage_label.config(text=network_usage)
        self.root.after(1000, self.update_network_usage)

if __name__ == "__main__":
    manager = NetworkManager()
    gui = NetworkGUI(manager)
