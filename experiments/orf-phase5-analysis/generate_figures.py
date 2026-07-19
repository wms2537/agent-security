import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "paper" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    "font.size": 6,
    "axes.titlesize": 7,
    "axes.labelsize": 6,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 5.5,
    "svg.hashsalt": "orf-phase5-iteration4-v1",
})


def read_tsv(relative_path):
    with (ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_source(basename, fieldnames, rows):
    path = FIGURES / f"{basename}.source.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig, basename):
    fig.tight_layout(pad=2)
    fig.savefig(FIGURES / f"{basename}.svg", metadata={"Date": None})
    fig.savefig(FIGURES / f"{basename}.png", dpi=300, metadata={"Date": None})
    plt.close(fig)


def comparison_chart():
    core = read_tsv("experiments/runs/orf-p4-core-v1/core-by-master.tsv")
    changed = read_tsv(
        "experiments/runs/orf-p4-generalization-v1/generalization-by-master.tsv"
    )
    comparison = read_tsv("experiments/orf-phase4-summary/comparison.tsv")
    core_mean = next(record["actual"] for record in comparison
                     if record["family"] == "primary")
    changed_mean = next(record["actual"] for record in comparison
                        if record["family"] == "generalization")
    groups = [
        ("Primary public", "P", core, "adaptive_gain_percent_decimal", core_mean),
        ("Changed public", "G", changed, "gain_percent_decimal", changed_mean),
    ]
    rows = []
    for regime, prefix, records, gain_key, group_mean in groups:
        for record in records:
            rows.append({
                "regime": regime,
                "master_label": f"{prefix}{record['master_index']}",
                "gain_percent": record[gain_key],
                "mean_gain_percent": group_mean,
                "materiality_threshold_percent": "5.000000000000",
            })
    write_source(
        "comparison_chart",
        ["regime", "master_label", "gain_percent", "mean_gain_percent",
         "materiality_threshold_percent"],
        rows,
    )

    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    colors = ["#176B87", "#D97706"]
    offsets = [-0.10, 0.0, 0.10]
    for x, (regime, _prefix, records, gain_key, group_mean_text) in enumerate(groups):
        values = [float(record[gain_key]) for record in records]
        group_mean = float(group_mean_text)
        ax.scatter(
            [x + offset for offset in offsets], values, s=22,
            color=colors[x], edgecolor="white", linewidth=0.45, zorder=3,
        )
        ax.plot([x - 0.18, x + 0.18], [group_mean, group_mean],
                color="black", linewidth=1.6, zorder=4)
        ax.text(x, group_mean + 1.4, f"mean {group_mean:.1f}%",
                ha="center", va="bottom", fontsize=5.5)
    ax.axhline(5, color="#555555", linewidth=0.8, linestyle=(0, (3, 2)))
    ax.text(1.28, 6.2, "5% materiality threshold", ha="right",
            va="bottom", fontsize=5.2, color="#444444")
    ax.set_xticks([0, 1], ["Primary public\nmasters", "Changed public\nmasters"])
    ax.set_xlim(-0.38, 1.38)
    # Zero is shown because the pre-specified comparison and 5% materiality
    # threshold are ratio-scale reference points.
    ax.set_ylim(0, 55)
    ax.set_ylabel("Adaptive gain over global (%)")
    ax.set_title("Per-profile selection clears the materiality threshold")
    save_figure(fig, "comparison_chart")


def ablation_heatmap():
    records = read_tsv(
        "experiments/runs/orf-p4-ablations-v1/ablation-by-master.tsv"
    )
    comparison = read_tsv("experiments/orf-phase4-summary/comparison.tsv")
    order = ["no_cliff", "no_reset", "no_curvature", "no_novelty", "unsaturated"]
    labels = {
        "no_cliff": "Remove cliff",
        "no_reset": "Remove reset",
        "no_curvature": "Remove curvature",
        "no_novelty": "Remove novelty",
        "unsaturated": "Remove saturation",
    }
    by_condition = {
        condition: sorted(
            [record for record in records if record["ablation"] == condition],
            key=lambda record: int(record["master_index"]),
        )
        for condition in order
    }
    rows = []
    for condition in order:
        condition_mean = next(record["delta_vs_primary_core_pp"]
                              for record in comparison
                              if record["family"] == "ablation"
                              and record["condition"] == condition)
        for record in by_condition[condition]:
            rows.append({
                "condition": condition,
                "master_index": record["master_index"],
                "delta_vs_core_percentage_points": record["delta_percentage_points_decimal"],
                "mean_delta_vs_core_percentage_points": condition_mean,
            })
    write_source(
        "ablation_heatmap",
        ["condition", "master_index", "delta_vs_core_percentage_points",
         "mean_delta_vs_core_percentage_points"],
        rows,
    )

    fig, ax = plt.subplots(figsize=(3.5, 2.65))
    colors = ["#176B87", "#D97706", "#7C3AED"]
    markers = ["o", "s", "^"]
    y_positions = list(range(len(order)))
    for master_index in range(3):
        values = [
            float(by_condition[condition][master_index]["delta_percentage_points_decimal"])
            for condition in order
        ]
        ax.scatter(values, y_positions, s=18, color=colors[master_index],
                   marker=markers[master_index], label=f"Master {master_index}", zorder=3)
    condition_means = [
        float(next(record["delta_vs_primary_core_pp"] for record in comparison
                   if record["family"] == "ablation"
                   and record["condition"] == condition))
        for condition in order
    ]
    ax.scatter(condition_means, y_positions, s=28, color="black", marker="D",
               label="Mean", zorder=4)
    ax.axvline(0, color="#555555", linewidth=0.8)
    ax.set_yticks(y_positions, [labels[condition] for condition in order])
    ax.invert_yaxis()
    ax.set_xlim(-36, 7)
    ax.set_xlabel("Change from primary core gain (percentage points)")
    ax.set_title("Cliff and reset mechanisms dominate the OAT contribution")
    ax.legend(frameon=False, ncol=2, loc="lower left")
    save_figure(fig, "ablation_heatmap")


def scaling_curve():
    records = read_tsv("experiments/runs/orf-p4-scaling-v1/scaling-by-cell.tsv")
    comparison = read_tsv("experiments/orf-phase4-summary/comparison.tsv")
    sizes = [40, 160, 320]
    rows = []
    by_master = {}
    means = {}
    for size in sizes:
        cell_records = sorted(
            [record for record in records if int(record["profiles"]) == size],
            key=lambda record: int(record["master_index"]),
        )
        means[size] = next(record["actual"] for record in comparison
                           if record["family"] == "scaling"
                           and record["condition"] == f"N{size}")
        for record in cell_records:
            index = int(record["master_index"])
            value = float(record["gain_percent_decimal"])
            by_master.setdefault(index, {})[size] = value
            rows.append({
                "master_index": str(index),
                "profiles": str(size),
                "gain_percent": record["gain_percent_decimal"],
                "mean_gain_percent": means[size],
            })
    write_source(
        "scaling_curve",
        ["master_index", "profiles", "gain_percent", "mean_gain_percent"],
        rows,
    )

    fig, ax = plt.subplots(figsize=(3.5, 2.55))
    colors = ["#176B87", "#D97706", "#7C3AED"]
    markers = ["o", "s", "^"]
    for master_index in range(3):
        values = [by_master[master_index][size] for size in sizes]
        ax.plot(sizes, values, color=colors[master_index], marker=markers[master_index],
                linewidth=0.9, markersize=3.4, label=f"Master {master_index}")
    ax.plot(sizes, [float(means[size]) for size in sizes], color="black", marker="D",
            linewidth=1.8, markersize=3.8, label="Mean")
    ax.set_xticks(sizes)
    ax.set_xlim(20, 340)
    ax.set_ylim(36, 55)
    ax.set_xlabel("Profiles per fixed public master")
    ax.set_ylabel("Adaptive gain over global (%)")
    ax.set_title("Conditional-regret gain persists across nested scales")
    ax.legend(frameon=False, ncol=2, loc="upper right")
    save_figure(fig, "scaling_curve")


if __name__ == "__main__":
    comparison_chart()
    ablation_heatmap()
    scaling_curve()
