#!/usr/bin/env python
"""Plot education completion / graduation comparisons from a CSV file."""

import argparse
import sys
from textwrap import fill

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.offsetbox import AnchoredText


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"topic", "segment", "percentage", "source"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(
            f"CSV must include columns {sorted(required)}. Missing: {sorted(missing)}"
        )
    return df


def plot_demographics(df: pd.DataFrame) -> None:
    topics = df["topic"].unique()
    n = len(topics)
    fig, axes = plt.subplots(
        n,
        1,
        figsize=(10, 3.5 * n),
        squeeze=False,
        layout="constrained",
    )
    axes_flat = axes.ravel()

    cmap = plt.colormaps["viridis"]
    fig.get_layout_engine().set(h_pad=0.5, hspace=0.22, w_pad=0.3)

    for ax, topic in zip(axes_flat, topics):
        sub = df[df["topic"] == topic]
        segments = sub["segment"].tolist()
        values = sub["percentage"].astype(float).tolist()
        source = sub["source"].iloc[0]

        colors = [cmap(i / max(len(values) - 1, 1)) for i in range(len(values))]
        y = range(len(segments))
        bars = ax.barh(y, values, color=colors, edgecolor="black", linewidth=0.6, alpha=0.88)
        ax.set_yticks(y)
        ax.set_yticklabels(segments)
        ax.set_xlabel("Share (%)")
        max_v = max(values)
        # Room for bar-end labels (e.g. "67.6%") without clipping
        ax.set_xlim(0, max(100, max_v * 1.06) + 12)
        ax.set_title(fill(topic, width=52), fontsize=10.5)
        ax.grid(True, axis="x", alpha=0.35)
        ax.invert_yaxis()

        ax.bar_label(
            bars,
            labels=[f"{v:g}%" for v in values],
            padding=5,
            fontsize=9,
        )

        src_box = AnchoredText(
            fill(f"Source: {source}", width=34),
            loc="lower left",
            bbox_to_anchor=(1.02, 0.0),
            bbox_transform=ax.transAxes,
            borderpad=0.35,
            prop=dict(size=7, color="#404040"),
            frameon=True,
        )
        src_box.patch.set(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="#c8c8c8",
            alpha=0.96,
        )
        ax.add_artist(src_box)

    fig.suptitle(
        "Postsecondary completion / graduation comparisons",
        fontsize=12,
    )
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot grouped comparisons from CSV (one subplot per topic)."
    )
    parser.add_argument(
        "csv_path",
        help="Path to CSV with columns: topic, segment, percentage, source",
    )
    args = parser.parse_args()

    df = load_csv(args.csv_path)
    plot_demographics(df)


if __name__ == "__main__":
    main()
