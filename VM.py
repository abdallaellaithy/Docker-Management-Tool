import subprocess
import tkinter as tk
from tkinter import simpledialog
import sys

def create_vm_interactive():
    name = simpledialog.askstring("Input", "Enter VM name:")
    memory = simpledialog.askstring("Input", "Enter memory size in MB:")
    disk_size = simpledialog.askstring("Input", "Enter disk size in MB:")

    subprocess.run([r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe", "createvm", "--name", name, "--register"])
    subprocess.run(["VBoxManage", "modifyvm", name, "--memory", memory])
    subprocess.run(["VBoxManage", "createhd", "--filename", f"{name}.vdi", "--size", disk_size])
    subprocess.run(["VBoxManage", "storagectl", name, "--name", "SATA Controller", "--add", "sata"])
    subprocess.run(["VBoxManage", "storageattach", name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", f"{name}.vdi"])

def create_vm_from_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = dict(line.strip().split('=') for line in file.readlines())

            name = config.get('name', 'default_vm')
            memory = config.get('memory', '512')
            disk_size = config.get('disk_size', '10240')

            subprocess.run(["VBoxManage", "createvm", "--name", name, "--register"])
            subprocess.run(["VBoxManage", "modifyvm", name, "--memory", memory])
            subprocess.run(["VBoxManage", "createhd", "--filename", f"{name}.vdi", "--size", disk_size])
            subprocess.run(["VBoxManage", "storagectl", name, "--name", "SATA Controller", "--add", "sata"])
            subprocess.run(["VBoxManage", "storageattach", name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", f"{name}.vdi"])
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main_2():
    root = tk.Tk()
    root.withdraw()

    if len(sys.argv) == 1:
        create_vm_interactive()
    elif len(sys.argv) == 2:
        config_file = sys.argv[1]
        create_vm_from_config(config_file)
    else:
        print("Usage: python create_vm.py [config_file]")

if __name__ == "__main__":
    main_2()
