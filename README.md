## **Live App:** [CLICK HERE](https://notable-companies-8osrztbynwckpf5owolqwr.streamlit.app/)

# Notable Indian Companies — Analytics Dashboard

An interactive Streamlit dashboard for exploring and analysing a dataset of **493 notable Indian companies** across industries, cities, eras, and ownership types.

---

## Project Structure

```
.
├── dashboard.py                  # Main Streamlit app
├── notable_companies__1_.csv     # Dataset
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install streamlit plotly pandas
```

### 2. Run the app

Make sure `dashboard.py` and the CSV file are in the same folder, then:

```bash
streamlit run dashboard.py
```

The app opens automatically at `http://localhost:8501`.

---

## Dataset Overview

| Field | Description |
|---|---|
| `Name` | Company name |
| `Industry` | Broad industry category (e.g. Industrials, Technology) |
| `Sector` | More specific sector within the industry |
| `Headquarters` | City where the company is headquartered |
| `Founded` | Year the company was founded |
| `Notes` | Short description of what the company does |
| `Private/State` | `P` = Private, `S` = State-owned |
| `Active/Defunct` | `A` = Active, `D` = Defunct |

**Quick stats:** 493 companies · 15 industries · 30+ cities · founded between 1736 and 2021

---

## Dashboard Features

### Sidebar Filters
All charts and KPIs update live when you apply these filters:
- **Industry** — single-select dropdown
- **Headquarters city** — multi-select (pick multiple cities)
- **Ownership type** — Private / State-owned / All
- **Status** — Active / Defunct / All
- **Founded between** — year range slider

### KPI Cards
Five summary metrics at the top of the page:

| Card | Metric |
|---|---|
| Companies | Total matching current filters |
| Industries | Unique industry count |
| Cities | Unique HQ city count |
| Private-owned | % of filtered companies that are private |
| Oldest Founded | Earliest founding year in filtered set |

### Charts

| Section | Chart | Insight |
|---|---|---|
| Industry & City | Horizontal bar — companies per industry | Industrials & Consumer Goods dominate |
| Industry & City | Bar — top 12 HQ cities | Mumbai hosts ~30% of all companies |
| Ownership & Status | Pie — private vs state-owned split | 79% private |
| Ownership & Status | Donut — active vs defunct | 98% still active |
| Ownership & Status | Stacked bar — top industries by ownership | Energy & Utilities skew state-owned |
| Founding Timeline | Area chart — companies founded per year | Major boom period: 1975–2010 |
| Era Breakdown | Funnel — companies by era bucket | 1950–1990 is the densest founding window |
| Era Breakdown | Line — top 6 industries across eras | Industrials peaked early; Technology rose post-2000 |
| Treemap | Industry → City hierarchy | Drill into which cities dominate each industry |
| Sunburst | Ownership → Industry → City | Full 3-level breakdown in one interactive chart |

### Data Table
A searchable, scrollable table at the bottom lets you find any company by name or description keyword.

---

## Tech Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data loading and transformation |

---

## Notes

- A few rows in the `Founded` column contain annotation suffixes (e.g. `2005[4]`) or `?` values — these are cleaned automatically; affected rows are excluded from year-based charts but remain in all other views.
- The `Sector` column has 45 missing values; these rows are still included in all charts that don't use `Sector`.
