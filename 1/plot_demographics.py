#!/usr/bin/env python3
"""Plot median income vs graduation rate from a CSV file."""

import argparse
import sys

import matplotlib.pyplot as plt
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"group", "median_income", "graduation_pct"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(
            f"CSV must include columns {sorted(required)}. Missing: {sorted(missing)}"
        )
    return df


def plot_demographics(df: pd.DataFrame) -> None:
    df = df.copy()
    inc = df["median_income"]
    grad = df["graduation_pct"]

    fig, ax = plt.subplots(figsize=(8, 6))

    xmin_d, xmax_d = inc.min(), inc.max()
    span = xmax_d - xmin_d
    pad_x = span * 0.06 if span > 0 else 5000
    ax.set_xlim(xmin_d - pad_x, xmax_d + pad_x)
    ax.set_ylim(0, 100)
    x_left = ax.get_xlim()[0]

    guide_kw = dict(
        linestyle=":",
        color="#404040",
        linewidth=2.4,
        alpha=0.92,
        zorder=1,
    )
    for _, row in df.iterrows():
        xi, yi = row["median_income"], row["graduation_pct"]
        ax.plot([xi, xi], [0, yi], **guide_kw)
        ax.plot([x_left, xi], [yi, yi], **guide_kw)

    df_line = df.sort_values("median_income")
    ax.plot(
        df_line["median_income"],
        df_line["graduation_pct"],
        linestyle=":",
        color="#707070",
        linewidth=1,
        alpha=0.9,
        zorder=2,
    )

    ax.scatter(
        inc,
        grad,
        s=120,
        c=range(len(df)),
        cmap="viridis",
        alpha=0.85,
        edgecolors="black",
        linewidths=0.6,
        zorder=3,
    )

    for _, row in df.iterrows():
        ax.annotate(
            row["group"],
            (row["median_income"], row["graduation_pct"]),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=9,
            zorder=4,
        )

    ax.set_xlabel("Median Income ($)")
    ax.set_ylabel("Graduation Rate (%)")
    ax.set_title("Median Income vs Graduation Rate by Race")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.grid(True, alpha=0.35)
    fig.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot median income and graduation rate from CSV (one chart)."
    )
    parser.add_argument(
        "csv_path",
        help="Path to CSV with columns: group, median_income, graduation_pct",
    )
    args = parser.parse_args()

    df = load_csv(args.csv_path)
    plot_demographics(df)


if __name__ == "__main__":
    main()
