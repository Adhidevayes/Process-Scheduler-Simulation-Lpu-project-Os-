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

