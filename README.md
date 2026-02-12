# 🚲 CityBike — Bike-Sharing Analytics Platform

## 📌 Overview

**CityBike** is a Python data-analytics project that analyzes bike-sharing usage, operations, and business metrics.
The platform loads raw CSV data, cleans and analyzes trips, generates statistics, creates visualizations, and exports a summary report.

The goal of this project is to demonstrate practical skills in:

* Data cleaning and preprocessing with **Pandas**
* Numerical computation using **NumPy**
* Data visualization using **Matplotlib**
* Object-Oriented Programming concepts
* Git workflow and structured project development

---

## ⚙️ Features

### 📊 Data Processing & Analytics

* Load and inspect bike-sharing datasets
* Clean missing values and invalid records
* Compute business insights such as:

  * Peak usage hours
  * Busiest days of the week
  * Monthly trip trends
  * Top active users
  * Most common routes
  * Maintenance cost analysis

### 💰 Pricing (Strategy Pattern)

* Casual pricing strategy
* Member pricing strategy
* Peak hour pricing example
* Example single-trip cost calculation

### 📈 Visualizations

The project generates and saves charts automatically:

* Bar chart — Trips per station
* Line chart — Monthly trip trend
* Histogram — Trip duration distribution
* Box plot — Duration by user type

All figures are exported to:

```
output/figures/
```

### 📝 Reporting

A full analytics summary is exported to:

```
output/summary_report.txt
```

---

## 🗂️ Project Structure

```
citybike/
│
├── analyzer.py        # Data cleaning and analytics engine
├── numerical.py       # NumPy-based calculations
├── pricing.py         # Pricing strategies (OOP design)
├── visualization.py   # Matplotlib charts
├── main.py            # Entry point of the application
│
├── data/              # Input datasets
└── output/            # Generated reports and figures
```

---

## ▶️ How to Run

1. Install dependencies:

```
pip install pandas numpy matplotlib
```

2. Run the main pipeline:

```
python main.py
```

The script will:

* Load datasets
* Clean data
* Run analytics
* Generate charts
* Export the summary report

---

## 🧠 Concepts Demonstrated

* Data analysis workflow
* Pandas transformations & grouping
* NumPy vectorized operations
* Strategy Pattern (OOP)
* Modular Python project design
* Git version control with structured commits

---

## 📷 Example Output

After running the program you should find:

```
output/
 ├── figures/
 │    ├── trips_per_station.png
 │    ├── monthly_trend.png
 │    ├── duration_histogram.png
 │    └── duration_by_user_type.png
 └── summary_report.txt
```

---

## 👨‍💻 Author

Data Science & AI Student Project — CityBike Analytics Platform
