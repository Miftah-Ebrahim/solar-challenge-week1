# ☀️ Solar Challenge Dashboard

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An interactive dashboard for analyzing climate data and solar energy potential across West African countries**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Deployment](#-deployment) • [Documentation](#-documentation)

</div>

---

## 📊 Overview

The **Solar Challenge Dashboard** is a professional, data-driven web application built with Streamlit for exploring climate patterns in **Benin**, **Sierra Leone**, and **Togo**. It provides comprehensive analysis of temperature and wind speed data to support renewable energy planning decisions.

### 🎯 Key Capabilities

- **Multi-Country Comparison** - Analyze climate data across three West African nations
- **Interactive Visualizations** - Dynamic time series, box plots, and statistical charts
- **Flexible Filtering** - Filter by country, date range, and metric
- **Statistical Analysis** - Summary statistics, top records, and distribution analysis
- **Data Export** - Download filtered datasets in CSV format
- **Smart Data Loading** - Automatic fallback to Google Drive if local files are missing

---

## ✨ Features

### 📈 **Time Series Analysis**
- Line charts showing temperature and wind speed trends over time
- Interactive hover details and zoom capabilities
- Country-wise color coding for easy comparison
- Key metrics dashboard (average, max, min values)

### 📊 **Statistical Comparison**
- Box plots for distribution analysis
- Summary statistics by country (mean, median, std dev, min/max)
- Color-coded tables with gradient highlighting
- Outlier detection and visualization

### 🏆 **Top Records Analysis**
- Configurable top-N records display (5-50 records)
- Highest and lowest value comparisons
- Visual bar charts for extreme values
- Date and country attribution

### 📋 **Data Summary & Export**
- Complete dataset preview
- Data completeness metrics
- One-click CSV export functionality
- Real-time record counts

---

## 🖼️ Demo

### Dashboard Interface
```
┌─────────────────────────────────────────────────────────┐
│  ☀️ Solar Challenge Dashboard                          │
│  Interactive Analysis of Climate Data                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📈 Time Series  │  📊 Statistics  │  🏆 Top Records  │
│                                                         │
│  [Interactive Plotly Charts]                            │
│  [Real-time Filtering]                                  │
│  [Export Options]                                       │
└─────────────────────────────────────────────────────────┘
```

### Sidebar Controls
- 📍 **Country Selection** - Multi-select dropdown
- 📊 **Metric Selection** - Temperature or Wind Speed
- 📅 **Date Range Picker** - Custom date filtering
- 🔢 **Top-N Slider** - Adjustable record display

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Miftah-Ebrahim/solar-challenge-week1/
   cd SOLAR-CHALLENGE-WEEK1
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Dashboard**
   ```bash
   cd notebooks/app
   streamlit run main.py
   ```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
SOLAR-CHALLENGE-WEEK1/
├── data/                          # CSV data files (auto-downloaded if missing)
│   ├── benin_clean.csv
│   ├── sierra_leone_clean.csv
│   └── togo_clean.csv
├── notebooks/
│   └── app/
│       ├── main.py               # Main Streamlit application
│       └── utils.py              # Data loading and preprocessing utilities
├── src/                          # Additional Python modules (optional)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 💻 Usage

### Running Locally

```bash
# Navigate to app directory
cd notebooks/app

# Launch dashboard
streamlit run main.py
```

### Using the Dashboard

1. **Select Countries**: Choose one or more countries from the sidebar
2. **Pick a Metric**: Select Temperature (T2M) or Wind Speed (WS10M_MIN)
3. **Set Date Range**: Filter data by specific time period
4. **Explore Tabs**: 
   - 📈 View time series trends
   - 📊 Compare statistical distributions
   - 🏆 Analyze extreme values
   - 📋 Export filtered data

### Data Requirements

Each CSV file must contain the following columns:
- `YEAR` - Year (integer)
- `MO` - Month (1-12)
- `DY` - Day (1-31)
- `T2M` - Temperature at 2 meters (°C)
- `WS10M_MIN` - Minimum wind speed at 10 meters (m/s)

---

## ☁️ Deployment

### Streamlit Community Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `notebooks/app/main.py`
   - Click "Deploy"

3. **Automatic Data Loading**
   - If CSV files are not in the repository, the app automatically downloads them from Google Drive
   - First load may take 10-15 seconds for downloads
   - Subsequent loads use cached data

### Environment Variables (Optional)

For production deployments, you can set custom configurations in Streamlit Cloud:

```toml
[server]
maxUploadSize = 200

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

---

## 🛠️ Configuration

### Customizing Data Sources

To use different data sources, update `GDRIVE_URLS` in `utils.py`:

```python
GDRIVE_URLS = {
    'benin': 'YOUR_GOOGLE_DRIVE_LINK',
    'sierra_leone': 'YOUR_GOOGLE_DRIVE_LINK',
    'togo': 'YOUR_GOOGLE_DRIVE_LINK'
}
```

### Adding New Countries

1. Add CSV file to `data/` folder with naming convention: `{country_name}_clean.csv`
2. Update `GDRIVE_URLS` dictionary in `utils.py`
3. CSV will automatically appear in country selection dropdown

### Modifying Cache Duration

Adjust cache time-to-live in `utils.py`:

```python
@st.cache_data(ttl=7200)  # Cache for 2 hours instead of 1
```

---

## 📚 Documentation

### Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Streamlit** | Web framework | 1.29.0 |
| **Pandas** | Data manipulation | 2.1.4 |
| **Plotly** | Interactive visualizations | 5.18.0 |
| **Requests** | HTTP downloads | 2.31.0 |
| **NumPy** | Numerical computing | 1.26.2 |

### Key Functions

#### `load_country_data(country_name, data_dir)`
Loads CSV data for a specific country, with automatic Google Drive fallback.

#### `preprocess_data(df)`
Creates datetime index, handles missing values, and prepares data for analysis.

#### `filter_data(df, countries, date_range)`
Filters dataset by selected countries and date range.

#### `calculate_summary_stats(df, metric)`
Computes statistical summaries grouped by country.

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: Data file not found`
- **Solution**: Ensure CSV files are in `data/` folder or check internet connection for Google Drive downloads

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
- **Solution**: Activate virtual environment and run `pip install -r requirements.txt`

**Issue**: Port already in use
- **Solution**: Run `streamlit run main.py --server.port 8502`

**Issue**: Deprecated fillna warning
- **Solution**: Already fixed in latest version using `.ffill()` and `.bfill()`

### Getting Help

- 📧 Open an issue on GitHub
- 💬 Check [Streamlit Community Forum](https://discuss.streamlit.io)
- 📖 Review [Streamlit Documentation](https://docs.streamlit.io)

---


### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where applicable
- Update README for new features
- Test locally before pushing

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Data Source**: Solar Challenge Project - Week 1
- **Framework**: Built with [Streamlit](https://streamlit.io)
- **Visualizations**: Powered by [Plotly](https://plotly.com)
- **Region**: West Africa Climate Data (Benin, Sierra Leone, Togo)

---

## 📞 Contact

**Project Maintainer**: [Mifta Yibrahim]

- GitHub: [(https://github.com/Miftah-Ebrahim/)]
- Email: miftah6972@gmail.com
- LinkedIn: https://www.linkedin.com/in/miftah-ebrahim

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Built with ❤️ for renewable energy research in West Africa**

[Back to Top](#-solar-challenge-dashboard)

</div>