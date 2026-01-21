import os
import matplotlib
matplotlib.use("Agg")  # ✅ Safe for Flask

import matplotlib.pyplot as plt


def generate_error_chart(error_code_counts: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(9, 4.5))
    ax = plt.gca()

    # ✅ Background color
    ax.set_facecolor("#f8fafc")  # light gray-blue background

    if not error_code_counts:
        plt.title("HTTP Error Code Distribution (No Errors Found)", fontsize=14, fontweight="bold")
        plt.xlabel("Error Code")
        plt.ylabel("Count")
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        return

    sorted_items = sorted(error_code_counts.items(), key=lambda x: x[0])
    codes = [str(k) for k, v in sorted_items]
    counts = [v for k, v in sorted_items]

    # ✅ Single bar color
    bars = plt.bar(codes, counts, color="#2563eb")  # same color for all

    plt.title("HTTP Error Code Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Error Code", fontsize=11)
    plt.ylabel("Frequency", fontsize=11)

    # Labels on top
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def generate_request_method_chart(method_counts: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(9, 4.5))
    ax = plt.gca()

    # ✅ Background color
    ax.set_facecolor("#f8fafc")  # light gray-blue background

    if not method_counts:
        plt.title("Request Method Distribution (No Data)", fontsize=14, fontweight="bold")
        plt.xlabel("Request Method")
        plt.ylabel("Count")
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        return

    order = ["GET", "POST", "PUT", "DELETE"]
    methods = [m for m in order if m in method_counts]
    counts = [method_counts[m] for m in methods]

    # ✅ Single bar color
    bars = plt.bar(methods, counts, color="#2563eb")

    plt.title("Request Method Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Request Method", fontsize=11)
    plt.ylabel("Count", fontsize=11)

    # Labels on top
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
