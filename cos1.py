import tkinter as tk
from tkinter import ttk
import numpy as np
import psutil
import subprocess
import matplotlib.pyplot as plt
import csv

def display_output(output_text):
    popup = tk.Toplevel()
    popup.title("Verification")
    label = tk.Label(popup, text=output_text)
    label.pack()

def fetch_process_data():
    try:
        with open("output.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print("File 'output.csv' not found.")
        return None

def bankers_algorithm(available, allocated, max_claim):
    num_processes = len(allocated)
    num_resources = len(available)
    remaining_need = max_claim - allocated
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        safe_found = False
        for i in range(num_processes):
            if not finish[i] and all(remaining_need[i] <= available):
                available += allocated[i]
                finish[i] = True
                safe_sequence.append(i)
                safe_found = True
                break
        if not safe_found:
            break

    if len(safe_sequence) == num_processes:
        print("System is in a safe state")
        return safe_sequence 
    else:
        print("System is in an unsafe state. Deadlock detected.")
        return None
    if len(safe_sequence) == num_processes:
        output_text = "System is in a safe state"
    else:
        output_text = "System is in an unsafe state. Deadlock detected."
    display_output(output_text)

def plot_graph(allocated):
    # Normalize the usage values to percentages
    usage_types = ['CPU Usage Alloc', 'Memory Usage Alloc', 'GPU Usage Alloc']
    usage_values = np.sum(allocated, axis=0) / np.sum(allocated) * 100

    plt.bar(usage_types, usage_values)
    plt.ylim(0, 100)  # Set the maximum limit of y-axis to 100% for percentage values
    plt.xlabel('Resource Type')
    plt.ylabel('Usage (%)')
    plt.title('Resource Usage Allocation')
    plt.savefig('resource_usage_plot.png')



def run_algorithm():
    process_data = fetch_process_data()
    if process_data:
        try:
            num_processes = len(process_data)
            num_resources = 3
            cpu_usage, memory_usage = get_system_resource_usage()
            gpu_usage = 100
            available = np.array([cpu_usage, memory_usage, gpu_usage], dtype=np.float64)
            allocated = np.array([[float(row[1]), float(row[2]), float(row[3])] for row in process_data])
            max_claim = np.array([[float(row[4]), float(row[5]), float(row[6])] for row in process_data])
            safe_sequence = bankers_algorithm(available, allocated, max_claim)
            if safe_sequence is not None:
                results_window = tk.Toplevel()
                results_window.title("Algorithm Results")
                results_text = tk.Text(results_window, height=20, width=50)
                results_text.pack()

                def countdown(count):
                    if count >= 0:
                        results_text.delete('1.0', tk.END)
                        results_text.insert(tk.END, f"Verification begins in {count}\n")
                        results_window.after(1000, countdown, count - 1)
                        results_window.update_idletasks()
                    else:
                        verify_sequence(safe_sequence, allocated, available, process_data, results_text)

                countdown(5)
        except ValueError:
            print("Invalid data format in 'output.csv'.")
    else:
        print("No data found in 'output.csv'.")


def verify_sequence(safe_sequence, allocated, available, process_data, results_text, idx=0):
    if idx < len(safe_sequence):
        process_index = safe_sequence[idx]
        process_name = process_data[process_index][0]  # Process name at index 0
        results_text.insert(tk.END, f"Verified allocation for {process_name}\n")
        results_text.yview_moveto(1.0)
        root.after(1000, verify_sequence, safe_sequence, allocated, available, process_data, results_text, idx + 1)
    else:
        results_text.insert(tk.END, "All processes completed successfully. Sequence verified.\n")
        results_text.yview_moveto(1.0)

def get_system_resource_usage():
    cpu_usage = 100 - psutil.cpu_percent(interval=1)
    memory_usage = 100 - psutil.virtual_memory().percent
    return cpu_usage, memory_usage

def show_graph():
    process_data = fetch_process_data()
    if process_data:
        allocated = np.array([[float(row[2]), float(row[3]), float(row[4])] for row in process_data])
        plot_graph(allocated)

root = tk.Tk()
root.title("Deadlock Avoidance")

# Maximize the window
root.attributes('-zoomed', True)
tree = ttk.Treeview(root, columns=('CPU Usage Alloc', 'Memory Usage Alloc', 'GPU Usage Alloc', 'CPU Usage Max', 'Memory Usage Max', 'GPU Usage Max'))
tree.heading('#0', text='Process Name')
tree.heading('#1', text='CPU Usage Alloc')
tree.heading('#2', text='Memory Usage Alloc')
tree.heading('#3', text='GPU Usage Alloc')
tree.heading('#4', text='CPU Usage Max')
tree.heading('#5', text='Memory Usage Max')
tree.heading('#6', text='GPU Usage Max')

process_data = fetch_process_data()
if process_data:
    for idx, row in enumerate(process_data):
        tree.insert('', 'end', text=row[0], values=row[1:])  # Process name at index 0

tree.pack(fill='both', expand=True)

run_button = tk.Button(root, text="Run Algorithm", command=run_algorithm)
run_button.pack(side='top', fill='x', padx=10)
graph_button = tk.Button(root, text="Show Graph", command=show_graph)
graph_button.pack(side='top', fill='x', padx=10)
# Define a font style with Times New Roman and size 14
font_style = ("Times New Roman", 14, "bold")

style = ttk.Style()
style.configure("Treeview.Heading", font=font_style)

tree = ttk.Treeview(root, style="Treeview")

run_button.configure(font=font_style)
graph_button.configure(font=font_style)

root.mainloop()

