"""
Solar Challenge Dashboard - Data Utilities Module
==================================================
This module handles data loading, preprocessing, and transformation
for the Solar Challenge dashboard application.

Author: Professional Python Developer
Date: 2025
"""

import pandas as pd
import streamlit as st
from pathlib import Path
from typing import List, Tuple
import os
import requests
from io import StringIO


# Google Drive direct download URLs for CSV files
GDRIVE_URLS = {
    "benin": "https://drive.google.com/uc?export=download&id=1T2OO5m_3hYE_LVQnVmOzPxjcRTgPE8FV",
    "sierra_leone": "https://drive.google.com/uc?export=download&id=1_s2ECZVzZ5L_WuHXdG-3JEqDaz8GQXOx",
    "togo": "https://drive.google.com/uc?export=download&id=1CeTpyMCRZ_sakchtULK_IZb-3ECeZR72",
}


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_country_data(country_name: str, data_dir: str = None) -> pd.DataFrame:
    """
    Load CSV data for a specific country.

    Parameters:
    -----------
    country_name : str
        Name of the country (e.g., 'benin', 'sierra_leone', 'togo')
    data_dir : str, optional
        Path to data directory. If None, auto-detects from project structure.

    Returns:
    --------
    pd.DataFrame
        Loaded dataframe with country data

    Raises:
    -------
    FileNotFoundError
        If the CSV file doesn't exist
    """
    # Auto-detect data directory if not provided
    if data_dir is None:
        # Get the project root (2 levels up from app/)
        project_root = Path(__file__).parent.parent.parent
        data_dir = project_root / "data"
    else:
        data_dir = Path(data_dir)

    # Construct filename - match actual file naming convention
    filename = f"{country_name}_clean.csv"
    file_path = data_dir / filename

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    # Load CSV
    df = pd.read_csv(file_path)

    # Add country identifier - convert underscores to spaces and title case
    df["Country"] = country_name.replace("_", " ").title()

    return df


@st.cache_data(ttl=3600)
def load_all_countries(
    countries: List[str] = None, data_dir: str = None
) -> pd.DataFrame:
    """
    Load and combine data for multiple countries.

    Parameters:
    -----------
    countries : List[str], optional
        List of country names to load. If None, loads all available countries.
        Note: Use underscores in country names (e.g., 'sierra_leone', not 'sierra-leone')
    data_dir : str, optional
        Path to data directory. If None, auto-detects from project structure.

    Returns:
    --------
    pd.DataFrame
        Combined dataframe with all country data
    """
    # Default countries if none specified - match actual file names with underscores
    if countries is None:
        countries = ["benin", "sierra_leone", "togo"]

    # Normalize country names: replace hyphens with underscores for file matching
    countries = [country.replace("-", "_") for country in countries]

    # Auto-detect data directory if not provided
    if data_dir is None:
        project_root = Path(__file__).parent.parent.parent
        data_dir = project_root / "data"
    else:
        data_dir = Path(data_dir)

    # Load each country's data
    dataframes = []
    for country in countries:
        try:
            df = load_country_data(country, data_dir)
            dataframes.append(df)
        except FileNotFoundError as e:
            st.warning(f"⚠️ Could not load data for {country}: {e}")
            continue
        except Exception as e:
            st.error(f"❌ Error loading {country}: {type(e).__name__}: {e}")
            continue

    # Combine all dataframes
    if not dataframes:
        raise ValueError(
            "No data could be loaded. Check your data directory and file names."
        )

    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the combined dataset by creating datetime index and cleaning data.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw combined dataframe

    Returns:
    --------
    pd.DataFrame
        Preprocessed dataframe with datetime index
    """
    # Create a copy to avoid modifying original
    df_processed = df.copy()

    # Ensure required columns exist
    required_cols = ["YEAR", "MO", "DY", "T2M", "WS10M_MIN", "Country"]
    missing_cols = [col for col in required_cols if col not in df_processed.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Create datetime column
    df_processed["Timestamp"] = pd.to_datetime(
        df_processed[["YEAR", "MO", "DY"]].rename(
            columns={"YEAR": "year", "MO": "month", "DY": "day"}
        )
    )

    # Set timestamp as index
    df_processed = df_processed.set_index("Timestamp")

    # Sort by timestamp
    df_processed = df_processed.sort_index()

    # Handle missing values (forward fill, then backward fill)
    df_processed["T2M"] = df_processed["T2M"].ffill().bfill()
    df_processed["WS10M_MIN"] = df_processed["WS10M_MIN"].ffill().bfill()

    return df_processed


def filter_data(
    df: pd.DataFrame,
    countries: List[str],
    date_range: Tuple[pd.Timestamp, pd.Timestamp],
) -> pd.DataFrame:
    """
    Filter dataframe by selected countries and date range.

    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed dataframe with datetime index
    countries : List[str]
        List of countries to include
    date_range : Tuple[pd.Timestamp, pd.Timestamp]
        Start and end dates for filtering

    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    # Filter by countries
    df_filtered = df[df["Country"].isin(countries)].copy()

    # Filter by date range
    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered.index >= start_date) & (df_filtered.index <= end_date)
    ]

    return df_filtered


def get_metric_info(metric_key: str) -> dict:
    """
    Get metadata for a specific metric.

    Parameters:
    -----------
    metric_key : str
        Metric identifier ('T2M' or 'WS10M_MIN')

    Returns:
    --------
    dict
        Dictionary containing metric metadata (name, unit, description)
    """
    metrics = {
        "T2M": {
            "name": "Temperature at 2 Meters",
            "unit": "°C",
            "description": "Air temperature measured at 2 meters above ground level",
        },
        "WS10M_MIN": {
            "name": "Minimum Wind Speed at 10 Meters",
            "unit": "m/s",
            "description": "Minimum wind speed measured at 10 meters above ground level",
        },
    }

    return metrics.get(
        metric_key,
        {"name": metric_key, "unit": "", "description": "No description available"},
    )


def calculate_summary_stats(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """
    Calculate summary statistics for a metric grouped by country.

    Parameters:
    -----------
    df : pd.DataFrame
        Filtered dataframe
    metric : str
        Metric column name

    Returns:
    --------
    pd.DataFrame
        Summary statistics by country
    """
    summary = (
        df.groupby("Country")[metric]
        .agg(
            [
                ("Mean", "mean"),
                ("Median", "median"),
                ("Min", "min"),
                ("Max", "max"),
                ("Std Dev", "std"),
            ]
        )
        .round(2)
    )

    return summary


def get_top_n_records(
    df: pd.DataFrame, metric: str, n: int = 10, ascending: bool = False
) -> pd.DataFrame:
    """
    Get top N records for a specific metric.

    Parameters:
    -----------
    df : pd.DataFrame
        Filtered dataframe
    metric : str
        Metric column name
    n : int
        Number of top records to return
    ascending : bool
        If True, return lowest values; if False, return highest values

    Returns:
    --------
    pd.DataFrame
        Top N records with relevant columns
    """
    # Sort by metric
    df_sorted = df.sort_values(by=metric, ascending=ascending)

    # Select top N
    top_n = df_sorted.head(n)

    # Return relevant columns
    result = top_n[["Country", metric]].reset_index()
    result.columns = ["Date", "Country", metric]

    return result
