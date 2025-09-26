import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pygetwindow
import threading
import time

class KeepActiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keep Active Utility")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        self.is_running = False
        self.worker_thread = None
        self.window_vars = {}

        # --- Create UI Elements ---
        # Status bar (created first, packed last at the bottom of the root)
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Idle")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, padding="5")

        # Main frame that holds everything else
        self.main_frame = ttk.Frame(self.root, padding="10")

        # --- Bottom controls ---
        controls_frame = ttk.Frame(self.main_frame)
        
        # Buttons frame
        buttons_frame = ttk.Frame(controls_frame)
        self.start_button = ttk.Button(buttons_frame, text="Mulai", command=self.start_keeping_active)
        self.stop_button = ttk.Button(buttons_frame, text="Berhenti", command=self.stop_keeping_active, state="disabled")
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        self.stop_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

        # Interval setting
        self.interval_spinbox = ttk.Spinbox(controls_frame, from_=1, to=300, increment=1)
        self.interval_spinbox.set("10")
        ttk.Label(controls_frame, text="2. Interval (detik):").pack(anchor="w")
        self.interval_spinbox.pack(fill=tk.X, pady=(0, 5))
        buttons_frame.pack(fill=tk.X)

        # Refresh button
        self.refresh_button = ttk.Button(self.main_frame, text="Segarkan Daftar", command=self.populate_window_list)

        # --- Scrollable Checkbox Frame (middle, expanding part) ---
        canvas_frame = ttk.Frame(self.main_frame)
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Top label
        self.top_label = ttk.Label(self.main_frame, text="1. Pilih Jendela Aplikasi:")

        # --- Layout UI Elements (in correct order) ---
        # 1. Pack status bar to the bottom of the ROOT window.
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 2. Pack main frame to fill the rest of the ROOT window.
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 3. Pack controls from the BOTTOM of the main_frame UPWARDS.
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0))
        self.refresh_button.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

        # 4. Pack the label to the TOP of the main_frame.
        self.top_label.pack(side=tk.TOP, anchor="w")

        # 5. Pack the scrollable frame to fill the remaining space.
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

        self.populate_window_list()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def populate_window_list(self):
        self.status_var.set("Status: Menyegarkan daftar jendela...")
        self.root.update_idletasks()
        try:
            # Clear old widgets
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.window_vars.clear()

            windows = [win for win in pygetwindow.getAllTitles() if win]
            for title in windows:
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.scrollable_frame, text=title, variable=var)
                checkbox.pack(anchor="w", fill="x", padx=5)
                self.window_vars[title] = var
            self.status_var.set("Status: Idle")
        except Exception as e:
            self.status_var.set(f"Error: {e}")

    def start_keeping_active(self):
        target_titles = [title for title, var in self.window_vars.items() if var.get()]
        
        if not target_titles:
            messagebox.showwarning("Peringatan", "Silakan pilih satu atau lebih jendela aplikasi.")
            return

        try:
            interval = int(self.interval_spinbox.get())
        except ValueError:
            messagebox.showwarning("Peringatan", "Interval harus berupa angka.")
            return

        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.refresh_button.config(state="disabled")
        
        for child in self.scrollable_frame.winfo_children():
            child.config(state="disabled")

        self.status_var.set(f"Aktif: Menjaga {len(target_titles)} jendela...")

        self.worker_thread = threading.Thread(target=self.keep_alive_worker, args=(target_titles, interval), daemon=True)
        self.worker_thread.start()

    def stop_keeping_active(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.refresh_button.config(state="normal")

        for child in self.scrollable_frame.winfo_children():
            child.config(state="normal")
            
        self.status_var.set("Status: Dihentikan")

    def keep_alive_worker(self, target_titles, interval):
        while self.is_running:
            try:
                active_window = pygetwindow.getActiveWindow()
                if active_window and active_window.title in target_titles:
                    # Simulasikan pergerakan mouse kecil untuk menandakan aktivitas
                    pyautogui.move(1, 0, duration=0.1)
                    pyautogui.move(-1, 0, duration=0.1)
            except Exception:
                # Abaikan jika ada error (misal: jendela target ditutup)
                pass
            time.sleep(interval)

    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("Keluar", "Skrip masih berjalan. Anda yakin ingin keluar?"):
                self.is_running = False
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    # Set failsafe to False because this app runs in the background
    pyautogui.FAILSAFE = False
    root = tk.Tk()
    app = KeepActiveApp(root)
    root.mainloop()