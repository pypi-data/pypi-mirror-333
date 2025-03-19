import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
from .meditation_generator import MeditationScriptGenerator

class MeditationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meditation Script Generator")
        self.root.geometry("800x600")
        self.generator = MeditationScriptGenerator()
        self.timer_running = False
        self.remaining_time = 0
        self.timer_thread = None
        
        self.setup_gui()
        
    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure("TCheckbutton", font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Meditation Script Generator", 
                              font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Needs selection
        needs_frame = ttk.LabelFrame(main_frame, text="Select Your Needs", padding="5")
        needs_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.need_vars = {
            "stress": tk.BooleanVar(),
            "anxiety": tk.BooleanVar(),
            "self_confidence": tk.BooleanVar(),
            "sleep": tk.BooleanVar()
        }
        
        for i, (need, var) in enumerate(self.need_vars.items()):
            need_name = need.replace("_", " ").title()
            ttk.Checkbutton(needs_frame, text=need_name, variable=var).grid(
                row=i//2, column=i%2, sticky=tk.W, padx=5)
        
        # Duration selection
        duration_frame = ttk.Frame(main_frame)
        duration_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Label(duration_frame, text="Duration (minutes):").grid(row=0, column=0)
        self.duration_var = tk.StringVar(value="10")
        duration_spinbox = ttk.Spinbox(duration_frame, from_=1, to=60, 
                                     textvariable=self.duration_var, width=5)
        duration_spinbox.grid(row=0, column=1, padx=5)
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Script", 
                                command=self.generate_script)
        generate_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Script display
        self.script_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                   width=70, height=15)
        self.script_text.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Timer display
        self.timer_label = ttk.Label(main_frame, text="Time remaining: 0:00", 
                                   font=("Arial", 14))
        self.timer_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Timer controls
        timer_frame = ttk.Frame(main_frame)
        timer_frame.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.start_timer_btn = ttk.Button(timer_frame, text="Start Meditation", 
                                        command=self.start_timer)
        self.start_timer_btn.grid(row=0, column=0, padx=5)
        
        self.stop_timer_btn = ttk.Button(timer_frame, text="Stop", 
                                       command=self.stop_timer, state=tk.DISABLED)
        self.stop_timer_btn.grid(row=0, column=1, padx=5)
        
    def generate_script(self):
        selected_needs = [need for need, var in self.need_vars.items() if var.get()]
        
        if not selected_needs:
            messagebox.showwarning("No Selection", 
                                 "Please select at least one meditation need.")
            return
        
        try:
            duration = int(self.duration_var.get())
            if duration < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Duration", 
                               "Please enter a valid duration (1-60 minutes).")
            return
        
        script = self.generator.generate_script(selected_needs, duration)
        self.script_text.delete(1.0, tk.END)
        self.script_text.insert(tk.END, script)
        
    def update_timer(self):
        while self.timer_running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"Time remaining: {mins}:{secs:02d}")
            time.sleep(1)
            self.remaining_time -= 1
            
        if self.remaining_time <= 0:
            self.timer_running = False
            self.timer_label.config(text="Meditation complete!")
            self.start_timer_btn.config(state=tk.NORMAL)
            self.stop_timer_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Meditation Complete", 
                              "Your meditation session has ended.")
    
    def start_timer(self):
        try:
            duration = int(self.duration_var.get())
            if duration < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Duration", 
                               "Please enter a valid duration (1-60 minutes).")
            return
        
        self.remaining_time = duration * 60
        self.timer_running = True
        self.start_timer_btn.config(state=tk.DISABLED)
        self.stop_timer_btn.config(state=tk.NORMAL)
        
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def stop_timer(self):
        self.timer_running = False
        self.timer_label.config(text="Time remaining: 0:00")
        self.start_timer_btn.config(state=tk.NORMAL)
        self.stop_timer_btn.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = MeditationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 