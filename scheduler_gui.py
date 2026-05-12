import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



# Process Class
class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid
        self.arrival = at
        self.burst = bt
        self.remaining = bt
        self.waiting = 0
        self.turnaround = 0



# Algorithms
def fcfs(processes):
    processes.sort(key=lambda x: x.arrival)
    time = 0
    gantt = []

    for p in processes:
        if time < p.arrival:
            time = p.arrival
        gantt.append((p.pid, time, time + p.burst))
        time += p.burst
        p.turnaround = time - p.arrival
        p.waiting = p.turnaround - p.burst

    return gantt, processes


def round_robin(processes, q):
    time = 0
    queue, completed, gantt = [], [], []
    processes.sort(key=lambda x: x.arrival)

    while processes or queue:
        while processes and processes[0].arrival <= time:
            queue.append(processes.pop(0))

        if queue:
            p = queue.pop(0)
            run = min(q, p.remaining)
            gantt.append((p.pid, time, time + run))
            time += run
            p.remaining -= run

            while processes and processes[0].arrival <= time:
                queue.append(processes.pop(0))

            if p.remaining > 0:
                queue.append(p)
            else:
                p.turnaround = time - p.arrival
                p.waiting = p.turnaround - p.burst
                completed.append(p)
        else:
            time += 1

    return gantt, completed


def sjf(processes):
    time = 0
    ready, completed, gantt = [], [], []
    processes.sort(key=lambda x: x.arrival)

    while processes or ready:
        while processes and processes[0].arrival <= time:
            ready.append(processes.pop(0))

        if ready:
            ready.sort(key=lambda x: x.burst)
            p = ready.pop(0)
            gantt.append((p.pid, time, time + p.burst))
            time += p.burst
            p.turnaround = time - p.arrival
            p.waiting = p.turnaround - p.burst
            completed.append(p)
        else:
            time += 1

    return gantt, completed


# UI FUNCTIONS
def get_data():
    data = []
    try:
        for i, (a, b) in enumerate(entries):
            data.append(Process(i+1, int(a.get()), int(b.get())))
        return data
    except:
        messagebox.showerror("Error", "Enter valid numbers")
        return None


def update_table(tree, processes):
    for row in tree.get_children():
        tree.delete(row)
    for p in processes:
        tree.insert("", "end", values=(p.pid, p.arrival, p.burst, p.waiting, p.turnaround))



# SHOW / HIDE TABLES
def show_only(frame):
    frame_fcfs.pack_forget()
    frame_sjf.pack_forget()
    frame_rr.pack_forget()
    frame.pack(fill="x", pady=10)


def show_all():
    frame_fcfs.pack(fill="x", pady=10)
    frame_sjf.pack(fill="x", pady=10)
    frame_rr.pack(fill="x", pady=10)



# GRAPH
def draw_chart(gantt):
    for w in chart_frame.winfo_children():
        w.destroy()

    fig, ax = plt.subplots(figsize=(6,3))

    for pid, start, end in gantt:
        ax.barh(0, end-start, left=start)
        ax.text((start+end)/2, 0, f"P{pid}",
                ha='center', va='center',
                color="white", fontweight="bold")

    ax.set_facecolor("#222")
    fig.patch.set_facecolor("#222")
    ax.set_title("Gantt Chart", color="white")
    ax.set_yticks([])
    ax.tick_params(colors='white')

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def compare_chart(g1, g2, g3, a1, a2, a3):
    for w in chart_frame.winfo_children():
        w.destroy()

    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,6))

    y = [2,1,0]
    labels = ["FCFS","SJF","RR"]

    for y_pos, gantt in zip(y, [g1,g2,g3]):
        for pid, start, end in gantt:
            ax1.barh(y_pos, end-start, left=start)
            ax1.text((start+end)/2, y_pos, f"P{pid}",
                     ha='center', va='center', color="white", fontweight="bold")

    ax1.set_yticks(y)
    ax1.set_yticklabels(labels, color="white")
    ax1.set_title("Gantt Comparison", color="white")

    vals = [a1,a2,a3]
    ax2.bar(["FCFS","SJF","RR"], vals)

    for i,v in enumerate(vals):
        ax2.text(i, v+0.2, f"{v:.2f}", ha='center', color="white")

    ax2.set_title("Average Waiting Time", color="white")

    for ax in (ax1,ax2):
        ax.set_facecolor("#222")
        ax.tick_params(colors='white')

    fig.patch.set_facecolor("#222")

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)



# ACTIONS
def run_algo():
    processes = get_data()
    if not processes:
        return

    algo = algo_box.get()

    if algo == "FCFS":
        gantt, res = fcfs(processes)
        update_table(tree_fcfs, res)
        show_only(frame_fcfs)

    elif algo == "SJF":
        gantt, res = sjf(processes)
        update_table(tree_sjf, res)
        show_only(frame_sjf)

    else:
        try:
            q = int(quantum.get())
        except:
            messagebox.showerror("Error","Invalid quantum")
            return

        gantt, res = round_robin(processes, q)
        update_table(tree_rr, res)
        show_only(frame_rr)

    draw_chart(gantt)


def compare_algorithms():
    processes = get_data()
    if not processes:
        return

    try:
        q = int(quantum.get())
    except:
        q = 2

    g1,r1 = fcfs(copy.deepcopy(processes))
    g2,r2 = sjf(copy.deepcopy(processes))
    g3,r3 = round_robin(copy.deepcopy(processes), q)

    update_table(tree_fcfs, r1)
    update_table(tree_sjf, r2)
    update_table(tree_rr, r3)

    show_all()

    a1 = sum(p.waiting for p in r1)/len(r1)
    a2 = sum(p.waiting for p in r2)/len(r2)
    a3 = sum(p.waiting for p in r3)/len(r3)

    compare_chart(g1,g2,g3,a1,a2,a3)
