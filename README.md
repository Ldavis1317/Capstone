# ⚾ Trackman Pitching Analysis Dashboard

## 📊 Overview
The **Trackman Pitching Analysis Dashboard** is a web-based analytics tool designed to help baseball players, coaches, and analysts evaluate pitching performance using Trackman CSV data.

By uploading a CSV file, users can visualize pitch metrics, analyze strengths and weaknesses, and receive data-driven coaching recommendations—all in an interactive dashboard.

---

## 🚀 Features

### 📈 Dashboard Visualizations
- **Pitch Usage Pie Chart** – Shows pitch mix distribution  
- **Velocity Bar Chart** – Displays average velocity per pitch type  
- **Spray Chart** – Visualizes batted ball locations  
- **Pitch Location Heatmap** – Shows pitch placement within the strike zone  

### 📉 Performance Metrics
- Total pitches thrown  
- Average velocity (MPH)  
- Average spin rate (RPM)  
- Strike percentage  
- Whiff percentage  

### ⚖️ Pitch Comparison
- Compares each pitch type to **optimal benchmarks**  
- Metrics included:
  - Velocity vs optimal  
  - Spin rate vs optimal  
  - Strike % and Whiff %  
- Assigns a **letter grade (A–D)** for each pitch  

### 🧠 Coaching Recommendations
- Identifies:
  - Best pitch  
  - Weakest pitch  
- Generates personalized recommendations based on:
  - Command (strike %)  
  - Swing-and-miss ability (whiff %)  
  - Velocity and spin efficiency  

### 🤖 Machine Learning Module
- Compares **actual vs predicted pitch locations**  
- Displays:
  - Average X error  
  - Average Z error  
  - Average distance error  
- Interactive scatter plot with:
  - Actual vs predicted points  
  - Connection lines between them  
- Adjustable sample size (10–100 pitches)  

---

## 📂 How It Works

1. Upload a **Trackman CSV file**  
2. The app uses:
   - **PapaParse** → to parse CSV data  
   - **Chart.js** → to generate visualizations  
3. Data is processed in real-time using JavaScript  
4. Results are displayed across multiple tabs:
   - Dashboard  
   - Performance  
   - Pitch Comparison  
   - Recommendations  
   - ML Model  

---

## 📄 Required CSV Fields

To fully utilize all features, your CSV should include:

### Core Pitch Data
- `pitch_type`  
- `release_speed`  
- `release_spin_rate`  
- `description`  

### Batted Ball Data (for spray chart)
- `hc_x`  
- `hc_y`  
- `events`  

### Pitch Location Data
- `plate_x`  
- `plate_z`  

### Machine Learning Predictions (optional)
- `pred_x`  
- `pred_z`  

---

## 🛠️ Technologies Used

- **HTML5** – App structure  
- **CSS3** – Styling and layout  
- **JavaScript (Vanilla)** – Data processing and logic  
- **Chart.js** – Data visualization  
- **PapaParse** – CSV parsing  

---

## 📦 Installation & Usage

### Run Locally
1. Clone or download this repository  
2. Make sure files are in the same directory:
3. Open `index.html` in your browser  

### Deploy Online
- Upload files to:
- GitHub Pages  
- Netlify  
- Vercel  

---

## 🎯 Use Cases

- Player development analysis  
- Coaching insights  
- Pitch design evaluation  
- Baseball analytics projects  
- Academic research presentations  

---

## ⚠️ Notes

- The ML Model tab requires `pred_x` and `pred_z`  
- Missing fields will limit certain visualizations  
- Runs entirely on the client (no backend required)  

---

## 🔮 Future Improvements

- Real machine learning model integration  
- Player comparison tools  
- Exportable reports (PDF/CSV)  
- Advanced pitch movement analytics  
- Team-wide dashboards  

---

## 👨‍💻 Author

Developed as a **baseball analytics project** combining sports performance and data science.
