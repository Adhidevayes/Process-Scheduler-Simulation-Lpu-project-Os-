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
