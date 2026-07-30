#!/usr/bin/env python3
"""Plot the D-Attn resolved-schedule-parameter sensitivity measurements.

Usage:
  python3 plot_scripts/plot_resolved_tiling_sensitivity.py
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


ROOT = Path("/mnt/workspace")
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ISOLATED = (
    ROOT
    / "ascendebug/logs/ifa_bmm1_three_groups_isolated_20260725_loop30"
    / "analysis_three_groups/speedup_by_shape.csv"
)
DEFAULT_GATE = (
    ROOT
    / "ascendebug/logs/ifa_bmm1_three_groups_gate_20260725_loop30"
    / "analysis_three_groups/speedup_by_shape.csv"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "figures/evaluation/op-speedup"
    / "resolved_constant_sensitivity"
)
TILINGINFER_CONSTANT_SCHEDULE_PARAMETERS = 352

GROUPS = [
    ("control_flow", "Control logic"),
    (
        "address_calculation",
        "Per-core tile dimensions/addressing",
    ),
    (
        "mm_schedule",
        "Core-loop scheduling/memory resources",
    ),
    ("three_group_joint", "Three groups jointly"),
    ("tilinginfer", "TilingInfer"),
]
DISPLAY_LABELS = {
    "control_flow": "Control logic",
    "address_calculation": "Per-core tile dimensions/addressing",
    "mm_schedule": "Core-loop scheduling/memory resources",
    "three_group_joint": "Three groups jointly",
    "tilinginfer": "TilingInfer",
}
PLOT_KV_LENGTHS = (512, 768, 1024, 1280)
GROUP_BACKGROUNDS = {
    "control_flow": "#F8D7DA",
    "address_calculation": "#D9EAD3",
    "mm_schedule": "#DDEBF7",
}
CASE_STYLES = [
    ("#0072B2", "o"),
    ("#D55E00", "s"),
    ("#009E73", "^"),
    ("#CC79A7", "D"),
    ("#E69F00", "P"),
]


@dataclass(frozen=True)
class Point:
    s_kv: int
    group: str
    speedup: float
    ci_low: float
    ci_high: float
    constant_fields: int
    baseline_mean_us: float
    specialized_mean_us: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--isolated-csv", type=Path, default=DEFAULT_ISOLATED)
    parser.add_argument("--gate-csv", type=Path, default=DEFAULT_GATE)
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--data-csv",
        type=Path,
        default=DEFAULT_OUTPUT.with_name(
            "resolved_constant_sensitivity_data.csv"
        ),
    )
    return parser.parse_args()


def read_points(path: Path, wanted: set[str]) -> list[Point]:
    points: list[Point] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "s_kv",
            "group",
            "speedup",
            "ci_low",
            "ci_high",
            "constant_fields",
            "baseline_mean_us",
            "specialized_mean_us",
            "correctness_pass",
        }
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns {sorted(missing)}")
        for row in reader:
            group = row["group"]
            if group not in wanted:
                continue
            if row["correctness_pass"].strip().lower() not in {"true", "1"}:
                raise ValueError(
                    f"{path}: correctness failed for {group}, S_KV={row['s_kv']}"
                )
            points.append(
                Point(
                    s_kv=int(row["s_kv"]),
                    group=group,
                    speedup=float(row["speedup"]),
                    ci_low=float(row["ci_low"]),
                    ci_high=float(row["ci_high"]),
                    constant_fields=int(row["constant_fields"]),
                    baseline_mean_us=float(row["baseline_mean_us"]),
                    specialized_mean_us=float(row["specialized_mean_us"]),
                )
            )
    return points


def validate(points: list[Point]) -> None:
    expected_groups = {group for group, _ in GROUPS}
    observed_groups = {point.group for point in points}
    if observed_groups != expected_groups:
        raise ValueError(
            f"expected groups {sorted(expected_groups)}, "
            f"found {sorted(observed_groups)}"
        )
    cases = sorted({point.s_kv for point in points})
    if cases != list(PLOT_KV_LENGTHS):
        raise ValueError(f"unexpected KV lengths: {cases}")
    keys = [(point.group, point.s_kv) for point in points]
    if len(keys) != len(set(keys)) or len(keys) != len(GROUPS) * len(cases):
        raise ValueError("expected one point per group and KV length")


def write_data(path: Path, points: list[Point]) -> None:
    labels = dict(GROUPS)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "s_kv",
                "group",
                "label",
                "speedup",
                "ci_low",
                "ci_high",
                "constant_fields",
                "baseline_mean_us",
                "specialized_mean_us",
            ]
        )
        for point in sorted(
            points,
            key=lambda item: (
                [group for group, _ in GROUPS].index(item.group),
                item.s_kv,
            ),
        ):
            writer.writerow(
                [
                    point.s_kv,
                    point.group,
                    labels[point.group],
                    point.speedup,
                    point.ci_low,
                    point.ci_high,
                    point.constant_fields,
                    point.baseline_mean_us,
                    point.specialized_mean_us,
                ]
            )


def plot(points: list[Point], output_stem: Path) -> None:
    cases = sorted({point.s_kv for point in points})
    by_key = {(point.group, point.s_kv): point for point in points}
    field_counts = {}
    for group, _ in GROUPS:
        counts = {
            point.constant_fields for point in points if point.group == group
        }
        if len(counts) != 1:
            raise ValueError(
                f"expected one constant-field count for {group}, "
                f"found {sorted(counts)}"
            )
        field_counts[group] = counts.pop()
    y_by_group = {
        group: len(GROUPS) - index - 1
        for index, (group, _) in enumerate(GROUPS)
    }
    offsets = np.linspace(-0.17, 0.17, len(cases))

    fig, ax = plt.subplots(figsize=(7.05, 2.04))
    ax.axhline(
        y_by_group["tilinginfer"] + 0.5,
        color="#9A9A9A",
        linewidth=0.7,
        zorder=0,
    )

    for case_index, s_kv in enumerate(cases):
        color, marker = CASE_STYLES[case_index]
        for group, _ in GROUPS:
            point = by_key[(group, s_kv)]
            ax.scatter(
                point.speedup,
                y_by_group[group] + offsets[case_index],
                s=30,
                color=color,
                marker=marker,
                edgecolor="white",
                linewidth=0.45,
                zorder=3,
            )

    values = [point.speedup for point in points]
    padding = max(0.009, (max(values) - min(values)) * 0.08)
    ax.set_xlim(min(1.0, min(values)) - padding, max(values) + padding)
    ax.set_ylim(-0.53, len(GROUPS) - 0.47)
    ax.axvline(
        1.0,
        color="#555555",
        linewidth=0.9,
        linestyle=(0, (3, 2)),
        zorder=1,
    )
    ax.xaxis.grid(True, color="#D9D9D9", linewidth=0.65, zorder=0)
    ax.yaxis.grid(False)

    ax.set_yticks(
        [y_by_group[group] for group, _ in GROUPS],
        [
            f"{DISPLAY_LABELS[group]} ({field_counts[group]})"
            for group, _ in GROUPS
        ],
    )
    ax.tick_params(axis="y", labelsize=8.0, length=0, pad=7)
    ax.tick_params(axis="x", labelsize=8.3)
    for tick_label, (group, _) in zip(ax.get_yticklabels(), GROUPS):
        if group in GROUP_BACKGROUNDS:
            tick_label.set_bbox(
                {
                    "facecolor": GROUP_BACKGROUNDS[group],
                    "edgecolor": "none",
                    "boxstyle": "round,pad=0.16",
                }
            )

    ax.set_xlabel(
        "Speedup over baseline \u2192 larger is better",
        fontsize=9.0,
        labelpad=3,
    )
    handles = [
        Line2D(
            [0],
            [0],
            marker=CASE_STYLES[index][1],
            color=CASE_STYLES[index][0],
            linestyle="none",
            markersize=5.3,
            markeredgecolor="white",
            markeredgewidth=0.45,
            label=f"KV length = {s_kv}",
        )
        for index, s_kv in enumerate(cases)
    ]
    ax.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.015),
        ncol=len(cases),
        frameon=False,
        fontsize=7.6,
        handletextpad=0.35,
        columnspacing=0.85,
        borderaxespad=0.0,
    )

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#777777")
    ax.spines["bottom"].set_linewidth(0.7)

    fig.subplots_adjust(left=0.37, right=0.985, bottom=0.235, top=0.75)
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(
        output_stem.with_suffix(".png"),
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


def main() -> None:
    args = parse_args()
    isolated = read_points(
        args.isolated_csv,
        {"control_flow", "address_calculation", "mm_schedule"},
    )
    gate = [
        replace(
            point,
            constant_fields=TILINGINFER_CONSTANT_SCHEDULE_PARAMETERS,
        )
        if point.group == "tilinginfer"
        else point
        for point in read_points(
            args.gate_csv,
            {"three_group_joint", "tilinginfer"},
        )
    ]
    points = isolated + gate
    points = [
        point for point in points if point.s_kv in PLOT_KV_LENGTHS
    ]
    validate(points)
    write_data(args.data_csv, points)
    plot(points, args.output_stem)
    print(f"wrote {args.data_csv}")
    print(f"wrote {args.output_stem}.pdf")
    print(f"wrote {args.output_stem}.png")


if __name__ == "__main__":
    main()
