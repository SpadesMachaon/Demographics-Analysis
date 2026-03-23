# Demographics-Analysis

Small Python utilities for visualizing U.S. education and income demographics from CSV data. The repository contains two self-contained examples in separate folders. Each folder has its own `plot_demographics.py` script and a sample `education_demographics.csv` that matches the schema that script expects.

## `1/` — Median income vs graduation rate

The script reads a table of demographic **groups** with **median household income** and **high school graduation rate** (or similar completion metric), then draws a scatter plot with guide lines connecting each point to the axes, a connecting trend line, and per-group labels.

**CSV columns:** `group`, `median_income`, `graduation_pct`

**Example:**

```bash
python 1/plot_demographics.py 1/education_demographics.csv
```

## `2/` — Postsecondary completion by topic

The script reads long-form rows grouped by **topic** (e.g. first-generation status, race, gender). For each topic it builds a horizontal bar chart of **percentage** shares by **segment**, with bar-end labels and a **source** citation box.

**CSV columns:** `topic`, `segment`, `percentage`, `source`

**Example:**

```bash
python 2/plot_demographics.py 2/education_demographics.csv
```

## Requirements

- Python 3
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

Install dependencies (for example):

```bash
pip install pandas matplotlib
```

Sample figures use illustrative public-statistics-style numbers; verify figures and citations against primary sources before publishing or citing in work.
