import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TrackManAnalysis:
    def __init__(self, root):
        self.root = root
        self.root.title("Trackman Pitching Analysis Development Program")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f0f0f0")

        # ===== HEADER =====
        header = tk.Frame(self.root, bg="#1f2c3c", pady=20)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Trackman Pitching Analysis Dashboard",
            fg="white",
            bg="#1f2c3c",
            font=("Helvetica", 20, "bold")
        ).pack()

        # ===== CONTROL PANEL =====
        control_panel = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        control_panel.pack(fill=tk.X)

        tk.Button(
            control_panel,
            text="Import Trackman CSV",
            command=self.import_csv,
            font=("Helvetica", 12),
            bg="#2980b9",
            fg="white",
            padx=20,
            pady=5
        ).pack()

        # ===== SCROLLABLE AREA =====
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # =============================
    # CSV IMPORT
    # =============================
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.plot_dashboard(df)
            except Exception as error:
                messagebox.showerror("Error", f"Could not read CSV: {error}")

    # =============================
    # MAIN DASHBOARD
    # =============================
    def plot_dashboard(self, df):

        required_cols = ['pitch_name', 'release_speed']
        if not all(col in df.columns for col in required_cols):
            messagebox.showwarning(
                "Warning",
                "CSV must contain 'pitch_name' and 'release_speed'."
            )
            return

        df = df.dropna(subset=required_cols)

        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # =============================
        # CHART SECTION
        # =============================
        usage = df['pitch_name'].value_counts()
        avg_speeds = df.groupby('pitch_name')['release_speed'].mean()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        plt.subplots_adjust(wspace=0.5, hspace=0.4)

        ax1.pie(usage, labels=usage.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Pitch Usage Mix (%)")

        bars = ax2.bar(avg_speeds.index, avg_speeds.values)
        ax2.set_title("Average Release Speed (MPH)")
        ax2.set_ylabel("MPH")

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.1f}', ha='center', va='bottom')

        plt.setp(ax2.get_xticklabels(), rotation=30)

        chart_canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(pady=20)

        # =============================
        # DASHBOARD METRICS
        # =============================
        metrics_frame = tk.Frame(self.scrollable_frame, bg="white")
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        def section_title(title):
            tk.Label(
                metrics_frame,
                text=title,
                font=("Helvetica", 16, "bold"),
                bg="white",
                fg="#1f2c3c",
                pady=10
            ).pack(anchor="w")

        def metric_card(parent, title, value, color="#2c3e50"):
            card = tk.Frame(parent, bg="#ecf0f1", bd=2, relief="ridge")
            card.pack(side=tk.LEFT, padx=10, pady=10)

            tk.Label(card, text=title,
                     font=("Helvetica", 10, "bold"),
                     bg="#ecf0f1",
                     fg=color).pack(padx=15, pady=(10, 0))

            tk.Label(card, text=value,
                     font=("Helvetica", 14),
                     bg="#ecf0f1").pack(padx=15, pady=(0, 10))

        # =============================
        # PERFORMANCE
        # =============================
        section_title("Performance Metrics")
        perf_frame = tk.Frame(metrics_frame, bg="white")
        perf_frame.pack(anchor="w")

        avg_vel = df['release_speed'].mean()
        vel_std = df['release_speed'].std()

        metric_card(perf_frame, "Avg Velocity", f"{avg_vel:.2f} MPH")
        metric_card(perf_frame, "Velocity Std Dev", f"{vel_std:.2f}")

        if 'release_spin_rate' in df.columns:
            metric_card(perf_frame, "Avg Spin Rate",
                        f"{df['release_spin_rate'].mean():.0f} RPM")

        if 'pfx_x' in df.columns and 'pfx_z' in df.columns:
            metric_card(perf_frame, "Avg Horizontal Break",
                        f"{df['pfx_x'].mean():.2f}")
            metric_card(perf_frame, "Avg Vertical Break",
                        f"{df['pfx_z'].mean():.2f}")

        # =============================
        # COMMAND
        # =============================
        section_title("Command & Release Metrics")
        cmd_frame = tk.Frame(metrics_frame, bg="white")
        cmd_frame.pack(anchor="w")

        if 'release_pos_x' in df.columns and 'release_pos_z' in df.columns:
            metric_card(cmd_frame, "Release X",
                        f"{df['release_pos_x'].mean():.2f}")
            metric_card(cmd_frame, "Release Z",
                        f"{df['release_pos_z'].mean():.2f}")

        if 'plate_x' in df.columns and 'plate_z' in df.columns:
            metric_card(cmd_frame, "Plate Location X",
                        f"{df['plate_x'].mean():.2f}")
            metric_card(cmd_frame, "Plate Location Z",
                        f"{df['plate_z'].mean():.2f}")

        # =============================
        # OUTCOMES
        # =============================
        section_title("Pitch Outcomes")
        outcome_frame = tk.Frame(metrics_frame, bg="white")
        outcome_frame.pack(anchor="w")

        if 'events' in df.columns:
            outcomes = df['events'].value_counts().head(5)
            for outcome, count in outcomes.items():
                metric_card(outcome_frame, outcome, str(count))

        # =============================
        # PROFILE RECOMMENDATION
        # =============================
        section_title("Pitch Profile Recommendation")

        profile_box = tk.Frame(metrics_frame, bg="#dfe6e9", bd=2, relief="solid")
        profile_box.pack(fill=tk.X, padx=10, pady=10)

        profile_text = ""

        if avg_vel > 93 and 'release_spin_rate' in df.columns and df['release_spin_rate'].mean() > 2200:
            profile_text = "Power Fastball Profile — Build arsenal around high velocity."
        elif 'pfx_x' in df.columns and abs(df['pfx_x'].mean()) > 10:
            profile_text = "Breaking Ball Specialist — Increase slider/curve usage."
        else:
            profile_text = "Command/Control Profile — Focus on sequencing and location."

        tk.Label(profile_box, text=profile_text,
                 font=("Helvetica", 12),
                 bg="#dfe6e9",
                 wraplength=900,
                 justify="left").pack(padx=15, pady=15)

        # =============================
        # INJURY RISK
        # =============================
        section_title("Injury Risk Assessment")

        injury_box = tk.Frame(metrics_frame, bd=2, relief="solid")
        injury_box.pack(fill=tk.X, padx=10, pady=10)

        injury_flag = False

        if vel_std > 3:
            injury_flag = True

        if 'release_pos_x' in df.columns and 'release_pos_z' in df.columns:
            release_consistency = df['release_pos_x'].std() + df['release_pos_z'].std()
            if release_consistency > 1.5:
                injury_flag = True

        if injury_flag:
            injury_box.configure(bg="#ff7675")
            injury_text = "⚠ Mechanical inconsistency detected — Monitor workload."
        else:
            injury_box.configure(bg="#55efc4")
            injury_text = "Delivery appears mechanically stable."

        tk.Label(injury_box, text=injury_text,
                 font=("Helvetica", 12, "bold"),
                 bg=injury_box["bg"],
                 wraplength=900,
                 justify="left").pack(padx=15, pady=15)

        # =============================
        # OPTIMAL METRICS COMPARISON BY PITCH TYPE
        # =============================
        section_title("Optimal Pitching Metrics Comparison (By Pitch Type)")

        optimal_box = tk.Frame(metrics_frame, bg="#f1f2f6", bd=2, relief="solid")
        optimal_box.pack(fill=tk.X, padx=10, pady=10)

                # Define optimal metrics per pitch type (example values)
        optimal_metrics_by_pitch = {
            "Fastball": {"Velocity": 95, "Spin Rate": 2300, "Horizontal Break": 2, "Vertical Break": 10},
            "4-Seam Fastball": {"Velocity": 96, "Spin Rate": 2350, "Horizontal Break": 1.5, "Vertical Break": 11},
            "Cutter": {"Velocity": 91, "Spin Rate": 2200, "Horizontal Break": 4, "Vertical Break": 8},
            "Sinker": {"Velocity": 92, "Spin Rate": 2250, "Horizontal Break": 3, "Vertical Break": 9},
            "Slider": {"Velocity": 87, "Spin Rate": 2500, "Horizontal Break": 5, "Vertical Break": 6},
            "Curveball": {"Velocity": 78, "Spin Rate": 2600, "Horizontal Break": 3, "Vertical Break": 8},
            "Changeup": {"Velocity": 83, "Spin Rate": 2100, "Horizontal Break": 2, "Vertical Break": 5},
            "Sweeper": {"Velocity": 85, "Spin Rate": 2450, "Horizontal Break": 6, "Vertical Break": 5}
        }

        comparison_text = ""
        recommendations = []

        pitch_types = df['pitch_name'].unique()
        for pitch in pitch_types:
            df_pitch = df[df['pitch_name'] == pitch]
            comparison_text += f"\n{pitch}:\n"

            opt = optimal_metrics_by_pitch.get(pitch, None)
            if not opt:
                comparison_text += "  No optimal data defined.\n"
                continue

            # Velocity
            avg_vel_pitch = df_pitch['release_speed'].mean()
            comparison_text += f"  Velocity: {avg_vel_pitch:.1f} MPH (Optimal: {opt['Velocity']} MPH)\n"
            if avg_vel_pitch < opt['Velocity']:
                recommendations.append(f"- {pitch}: Increase velocity through lower-body and core strength training.")

            # Spin Rate
            if 'release_spin_rate' in df.columns:
                avg_spin_pitch = df_pitch['release_spin_rate'].mean()
                comparison_text += f"  Spin Rate: {avg_spin_pitch:.0f} RPM (Optimal: {opt['Spin Rate']} RPM)\n"
                if avg_spin_pitch < opt['Spin Rate']:
                    recommendations.append(f"- {pitch}: Improve spin efficiency with grip and pronation mechanics.")

            # Horizontal Break
            if 'pfx_x' in df.columns:
                avg_hbreak = df_pitch['pfx_x'].mean()
                comparison_text += f"  Horizontal Break: {avg_hbreak:.2f}\" (Optimal: {opt['Horizontal Break']}\")\n"
                if abs(avg_hbreak) < opt['Horizontal Break']:
                    recommendations.append(f"- {pitch}: Adjust arm slot or pitch mechanics to increase horizontal break.")

            # Vertical Break
            if 'pfx_z' in df.columns:
                avg_vbreak = df_pitch['pfx_z'].mean()
                comparison_text += f"  Vertical Break: {avg_vbreak:.2f}\" (Optimal: {opt['Vertical Break']}\")\n"
                if abs(avg_vbreak) < opt['Vertical Break']:
                    recommendations.append(f"- {pitch}: Optimize spin axis and release point for more vertical break.")

        tk.Label(optimal_box, text=comparison_text,
                 font=("Helvetica", 12),
                 bg="#f1f2f6",
                 justify="left",
                 wraplength=900).pack(padx=15, pady=15)

        # =============================
        # RECOMMENDATIONS TO REACH OPTIMAL METRICS
        # =============================
        section_title("Recommendations to Reach Optimal Metrics")

        recommend_box = tk.Frame(metrics_frame, bg="#fef9e7", bd=2, relief="solid")
        recommend_box.pack(fill=tk.X, padx=10, pady=10)

        if not recommendations:
            recommendations.append("- All pitch metrics meet or exceed optimal values. Focus on consistency and command.")

        tk.Label(recommend_box, text="\n".join(recommendations),
                 font=("Helvetica", 12),
                 bg="#fef9e7",
                 justify="left",
                 wraplength=900).pack(padx=15, pady=15)


# ===== RUN APPLICATION =====
root = tk.Tk()
app = TrackManAnalysis(root)
root.mainloop()
