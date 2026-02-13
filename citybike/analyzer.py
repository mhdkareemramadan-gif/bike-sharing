"""
Data analysis engine for the CityBike platform.

Contains the BikeShareSystem class that orchestrates:
    - CSV loading and cleaning
    - Answering business questions using Pandas
    - Generating summary reports

Students should implement the cleaning logic and at least 10 analytics methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:
    """Central analysis class — loads, cleans, and analyzes bike-share data.

    Attributes:
        trips: DataFrame of trip records.
        stations: DataFrame of station metadata.
        maintenance: DataFrame of maintenance records.
    """
    # loads, cleans, inspects, analyzes bike-share data and generates reports
    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            print(f"\n{'='*40}")
            print(f"  {name}")
            print(f"{'='*40}")
            print(df.info())
            print(f"\nMissing values:\n{df.isnull().sum()}")
            print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """Clean all DataFrames and export to CSV.

        Steps to implement:
            1. Remove duplicate rows
            2. Parse date/datetime columns
            3. Convert numeric columns stored as strings
            4. Handle missing values (document your strategy!)
            5. Remove invalid entries (e.g. end_time < start_time)
            6. Standardize categorical values
            7. Export cleaned data to data/trips_clean.csv etc.

            """
        if self.trips is None:
            raise RuntimeError("Call load_data() first")

        # --- Step 1: Remove duplicates ---
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        # subset means we only consider the "trip_id" column for identifying duplicates
        print(f"After dedup: {self.trips.shape[0]} trips")

        # --- Step 2: Parse dates ---
        # TODO: convert start_time, end_time to datetime
        # self.trips["start_time"] = pd.to_datetime(...)
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"], errors="coerce")
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"], errors="coerce")
        #coerce : any invalid dates to NaT (Not a Time).

        # --- Step 3: Convert numeric columns ---
        # TODO: ensure duration_minutes and distance_km are float
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors="coerce")
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors="coerce")


        # --- Step 4: Handle missing values ---
        # TODO: decide on a strategy and document it
        # Example: self.trips["duration_minutes"].fillna(..., inplace=True)
        self.trips["status"] = self.trips["status"].fillna("unknown")
        self.trips["duration_minutes"] = self.trips["duration_minutes"].fillna(self.trips["duration_minutes"].mean())
        self.trips["distance_km"] = self.trips["distance_km"].fillna(self.trips["distance_km"].mean())


        # --- Step 5: Remove invalid entries ---
        # TODO: drop rows where end_time < start_time
        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]]
        # filter out invalid trips 


        # --- Step 6: Standardize categoricals ---
        # TODO: e.g. self.trips["status"].str.lower().str.strip()
        self.trips["status"] = self.trips["status"].str.lower().str.strip()
        self.trips["user_type"] = self.trips["user_type"].str.lower().str.strip()


        # --- Step 7: Export cleaned datasets ---
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)
        # index=False: it means that the row numbers (0, 1, 2, ...) will not be included in the output CSV file.

        print("Cleaning complete.")

    # ------------------------------------------------------------------
    # Analytics — Business Questions
    # ------------------------------------------------------------------

    def total_trips_summary(self):
        """Q1: Total trips, total distance, average duration.

        Returns:
            Dict with 'total_trips', 'total_distance_km', 'avg_duration_min'.
        """
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
                #rounding to 2 decimal places for better readability
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }



    def peak_usage_hours(self):
        """Q3: Trip count by hour of day.

        TODO: extract hour from start_time and count trips per hour.
        """
        df = self.trips.copy()
        df["hour"] = df["start_time"].dt.hour
        #.hour means we are extracting the hour from the start_time
        return df["hour"].value_counts().sort_index()
    


    def busiest_day_of_week(self) -> pd.Series:
        """Q4: Trip count by day of week.

        TODO: extract day-of-week from start_time, count.
        """
        df = self.trips.copy()

        df["day_name"] = df["start_time"].dt.day_name()

        return df["day_name"].value_counts()
    

    def avg_distance_by_user_type(self) -> pd.Series:
        """Q5: Average trip distance grouped by user type."""
        return self.trips.groupby("user_type")["distance_km"].mean().round(2)


    def monthly_trip_trend(self):
        """Q7: Monthly trip counts over time.

        TODO: extract year-month from start_time, group, count.
        """
        df = self.trips.copy()

        df["year_month"] = df["start_time"].dt.to_period("M")

        trend = df["year_month"].value_counts().sort_index()

        return trend
    #to_period means we are converting the start_time to a monthly period


    def top_active_users(self, n: int = 15):
        """Q8: Top *n* most active users by trip count.

        TODO: group by user_id, count trips, sort descending.
        """
        df = self.trips.copy()

        counts = (
            df.groupby("user_id")
            .size()
            #size means we are counting trips(rows) per group (user_id)
            .reset_index(name="trip_count")
            #.reset_index(name="trip_count") means we are converting the Series that comes from groupby back to a DataFrame
            .sort_values("trip_count", ascending=False)
            .head(n)
        )

        return counts
    


    def maintenance_cost_by_bike_type(self):
        """Q9: Total maintenance cost per bike type.

        TODO: group maintenance by bike_type, sum cost.
        """
        df = self.maintenance.copy()

        # df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
        #pd.to_numeric(...) means we are converting the cost column to numeric, forcing errors to NaN
        #errors='coerce' means that any non-numeric values will be replaced with NaN

        result = df.groupby("bike_type")["cost"].sum().round(2)

        return result
    


    def top_routes(self, n: int = 10):
        """Q10: Most common start→end station pairs.

        TODO: group by (start_station_id, end_station_id), count, sort.
        """
        df = self.trips.copy()

        routes = (
            df.groupby(["start_station_id", "end_station_id"])
            .size()
            .reset_index(name="trip_count")
            .sort_values("trip_count", ascending=False)
            .head(n)
        )

        return routes

    # ------------------------------------------------------------------
    # Add more analytics methods here
    # ------------------------------------------------------------------

    # Distribution of trips by user type.
    def user_type_distribution(self):
        return self.trips["user_type"].value_counts()
    

    # Distribution of trips by status.
    def status_distribution(self):
        return self.trips["status"].value_counts()

    # Longest trips by duration.
    def longest_trips(self, n: int = 10):
        infos = ["user_id", "bike_type", "start_time", "end_time", "duration_minutes", "distance_km"]
        return self.trips[infos].sort_values("duration_minutes", ascending=False).head(n)





    # ------------------------ Reporting ------------------------------------------
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """Write a summary text report to output/summary_report.txt.

        TODO:
            - Uncomment and complete each section below
            - Add results from remaining analytics methods
        """
    

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"
        # parent=True means we are creating any necessary parent directories
        # exist_ok=True means we won't raise an error if the directory already exists

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  CityBike — Summary Report")
        lines.append("=" * 60)

        # lines.append means we are adding a new line to the list of lines that will make up our report.
        # Each call to lines.append() adds a new line of text to the report.
        # For example, lines.append("=" * 60) adds a line of 60 equal signs as a separator,
        # and lines.append("  CityBike — Summary Report") adds the title of the report.

        # --- Q1: Overall summary ---
        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"  Total trips       : {summary['total_trips']}")
        lines.append(f"  Total distance    : {summary['total_distance_km']} km")
        lines.append(f"  Avg duration      : {summary['avg_duration_min']} min")
        
        # --- Q3: Peak usage hours ---
        # TODO: uncomment once peak_usage_hours() is implemented
        hours = self.peak_usage_hours()
        lines.append("\n--- Peak Usage Hours (Trips per Hour) ---")
        lines.append(hours.to_string()) 

        # --- Q9: Maintenance cost by bike type ---
        # TODO: uncomment once maintenance_cost_by_bike_type() is implemented
        maint_cost = self.maintenance_cost_by_bike_type()
        lines.append("\n--- Maintenance Cost by Bike Type ---")
        lines.append(maint_cost.to_string())

        # --- Q4: Busiest day of week ---
        days = self.busiest_day_of_week()
        lines.append("\n--- Trips per Day of Week ---")
        lines.append(days.to_string())

        # --- Q5: Avg distance by user type ---
        avg_dist = self.avg_distance_by_user_type()
        lines.append("\n--- Avg Distance by User Type (km) ---")
        lines.append(avg_dist.to_string())

        # --- Q7: Monthly trip trend ---
        monthly = self.monthly_trip_trend()
        lines.append("\n--- Monthly Trip Trend ---")
        lines.append(monthly.to_string())

        # --- Q8: Top active users ---
        top_users = self.top_active_users()
        lines.append("\n--- Top Active Users ---")
        lines.append(top_users.to_string(index=False))
        # to_string(index=False) ensures no index is printed



        # --- Q10: Top routes ---
        routes = self.top_routes()
        lines.append("\n--- Top Routes (Start -> End) ---")
        lines.append(routes.to_string(index=False))

        # TODO: add more sections for Q4–Q8, Q10–Q14 …

        # --- User Type Distribution ---
        lines.append("\n--- Trips by User Type ---")
        lines.append(self.user_type_distribution().to_string())

        # --- Status Distribution ---
        lines.append("\n--- Trips by Status ---")
        lines.append(self.status_distribution().to_string())

        # --- Longest Trips ---
        lines.append("\n--- Longest Trips ---")
        lines.append(self.longest_trips().to_string(index=False))


        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        
        print(f"Report saved to {report_path}")
