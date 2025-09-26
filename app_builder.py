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

        # --- UI Elements ---
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Window selection
        ttk.Label(self.main_frame, text="1. Pilih Jendela Aplikasi (tahan Ctrl/Shift untuk memilih lebih dari satu):").pack(anchor="w")
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.window_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, exportselection=False, height=5)
        self.window_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.window_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.window_listbox.config(yscrollcommand=scrollbar.set)


        self.refresh_button = ttk.Button(self.main_frame, text="Segarkan Daftar", command=self.populate_window_list)
        self.refresh_button.pack(fill=tk.X, pady=2)

        # Interval setting
        ttk.Label(self.main_frame, text="2. Interval (detik):").pack(anchor="w", pady=(10, 0))
        self.interval_spinbox = ttk.Spinbox(self.main_frame, from_=1, to=300, increment=1)
        self.interval_spinbox.set("10")
        self.interval_spinbox.pack(fill=tk.X)

        # Controls
        self.start_button = ttk.Button(self.main_frame, text="Mulai", command=self.start_keeping_active)
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=(10, 0), padx=(0, 5))

        self.stop_button = ttk.Button(self.main_frame, text="Berhenti", command=self.stop_keeping_active, state="disabled")
        self.stop_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, pady=(10, 0), padx=(5, 0))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Idle")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, padding="5")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.populate_window_list()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def populate_window_list(self):
        self.status_var.set("Status: Menyegarkan daftar jendela...")
        self.root.update_idletasks()
        try:
            self.window_listbox.delete(0, tk.END)
            windows = [win for win in pygetwindow.getAllTitles() if win]
            for window in windows:
                self.window_listbox.insert(tk.END, window)
            self.status_var.set("Status: Idle")
        except Exception as e:
            self.status_var.set(f"Error: {e}")

    def start_keeping_active(self):
        selected_indices = self.window_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Peringatan", "Silakan pilih satu atau lebih jendela aplikasi.")
            return
        
        target_titles = [self.window_listbox.get(i) for i in selected_indices]

        try:
            interval = int(self.interval_spinbox.get())
        except ValueError:
            messagebox.showwarning("Peringatan", "Interval harus berupa angka.")
            return

        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.refresh_button.config(state="disabled")
        self.window_listbox.config(state="disabled")

        self.status_var.set(f"Aktif: Menjaga {len(target_titles)} jendela...")

        self.worker_thread = threading.Thread(target=self.keep_alive_worker, args=(target_titles, interval), daemon=True)
        self.worker_thread.start()

    def stop_keeping_active(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.refresh_button.config(state="normal")
        self.window_listbox.config(state="normal")
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