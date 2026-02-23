import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#important notes for this application.
#Creating a py file allows us flexibility on deciding if we want a EXE file based application or a web based app.
#This code uses pandas for data manipulation. TKINTER for GUI and parsing the csv, matplotlib for graphs
#potential future libraries we will look at pybaseball(Perfect for us) SCIKit LEarn(ML), numpy(If we decide pandas isnt for us)
#This is currently coded for data charts from baseball savant, we will change this for trackman specific csv files once we get offical data.
#there is no machine learning model atm, we plan to use XGBoost as it has linear regression and other model types which are great for predictions and trends.
#We will code a more indepth program as we approach the end of midterms as well as closer to the final presentation. 

class TrackManAnalysis:
    '''This Class Creates an Application Window that will import a csv file and return charts and graphs to display metrics to the baseball team.'''
    def __init__(self, root):
        self.root = root
        self.root.title("Trackman Pitching Analysis Devlopment Program")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f0f0")
        self.header = tk.Frame(self.root, bg="#2c3e50", pady=20)
        self.header.pack(fill=tk.X)

        self.title_label = tk.Label(self.header, text="Trackman Pitching Analysis Devlopment Program", 
                                    fg="white", bg="#2c3e50", font=("Helvetica", 20, "bold"))
        self.title_label.pack()

        self.control_panel = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        self.control_panel.pack(fill=tk.X)

        self.import_btn = tk.Button(self.control_panel, text="Import Trackman Data Sheet (CSV)", 
                                    command=self.import_csv, font=("Helvetica", 12),
                                    bg="#3498db", fg="white", padx=20, pady=5)
        self.import_btn.pack()

        self.canvas_frame = tk.Frame(self.root, bg="white")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def import_csv(self):
        '''Creates a button that allows a user to import a CSV file to be read and parsed.'''
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.plot_charts(df)
            except Exception as error:
                messagebox.showerror("Error", f"The CSV file could not be read: {error}")

    def plot_charts(self, df):
        '''This method cleans the data, creates charts and graphs, then plots them.'''
        required_cols = ['pitch_name', 'release_speed']
        if not all(col in df.columns for col in required_cols):
            messagebox.showwarning("Warning", "The CSV structure is missing 'pitch_name' or 'release_speed'.")
            return

        df = df.dropna(subset=required_cols)

        usage = df['pitch_name'].value_counts()
        
        avg_speeds = df.groupby('pitch_name')['release_speed'].mean().sort_values(ascending=False)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        plt.subplots_adjust(wspace=0.3)

        colors = plt.cm.Set3(range(len(usage)))
        ax1.pie(usage, labels=usage.index, autopct='%1.1f%%', startangle=90, 
                colors=colors, wedgeprops={'edgecolor': 'white'})
        ax1.set_title("Pitch Usage Mix (%)", fontsize=14, fontweight='bold', pad=20)

        bar_colors=plt.cm.tab10(range(len(avg_speeds)))
        bars = ax2.bar(avg_speeds.index, avg_speeds.values, color=bar_colors, edgecolor='#d35400')
        ax2.set_title("Average Release Speed (MPH)", fontsize=14, fontweight='bold', pad=20)
        ax2.set_ylabel("MPH")
        ax2.set_ylim(min(avg_speeds.values) - 5, max(avg_speeds.values) + 5)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

        plt.setp(ax2.get_xticklabels(), rotation=30, horizontalalignment='right')

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
app = TrackManAnalysis(root)
root.mainloop()