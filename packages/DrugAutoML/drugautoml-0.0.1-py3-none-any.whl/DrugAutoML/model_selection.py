import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve

# Use default ggplot style
plt.style.use("ggplot")
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11
})

def model_selection_report(cv_results, results_folder="results"):
    """
    Generates a validation report by constructing a summary DataFrame and a grouped bar chart with error bars.
    Saves the summary table to "validation_metrics.csv" and the plot to "validation_metrics.png".

    Parameters:
      cv_results (dict): Cross-validation results for each model.
      results_folder (str): Folder to store output files.

    Returns:
      pd.DataFrame: Summary DataFrame with validation metrics.
    """
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    metrics = [
        ("accuracy", "Accuracy"),
        ("precision", "Precision"),
        ("recall", "Recall"),
        ("f1", "F1"),
        ("roc_auc", "AUC-ROC"),
        ("average_precision", "PRC-AUC"),
        ("mcc", "MCC"),
        ("cohen_kappa", "Cohen Kappa")
    ]

    rows = []
    model_names = []
    colors = plt.cm.tab10(np.linspace(0, 1, len(metrics)))

    metric_means_for_plot = {display: [] for _, display in metrics}
    metric_stds_for_plot = {display: [] for _, display in metrics}

    for model_name, result_dict in cv_results.items():
        mean_metrics = result_dict["mean_metrics"]
        std_metrics = result_dict["std_metrics"]

        row_data = {"Model": model_name}
        for (metric_key, metric_display) in metrics:
            mean_key = f"{metric_key}_cv_mean"
            std_key = f"{metric_key}_cv_stdev"
            mean_val = mean_metrics.get(mean_key, np.nan)
            std_val = std_metrics.get(std_key, np.nan)
            row_data[metric_display] = f"{mean_val:.4f} ± {std_val:.4f}"
            metric_means_for_plot[metric_display].append(mean_val)
            metric_stds_for_plot[metric_display].append(std_val)

        rows.append(row_data)
        model_names.append(model_name)

    summary_df = pd.DataFrame(rows)
    table_path = os.path.join(results_folder, "validation_metrics.csv")
    summary_df.to_csv(table_path, index=False)

    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(model_names))
    bar_width = 0.08

    for i, (_, metric_display) in enumerate(metrics):
        means = metric_means_for_plot[metric_display]
        stds = metric_stds_for_plot[metric_display]
        ax.bar(
            x + i * bar_width, means, yerr=stds,
            width=bar_width, label=metric_display,
            capsize=4, alpha=0.85, color=colors[i]
        )

    ax.set_xticks(x + bar_width * (len(metrics) - 1) / 2.0)
    ax.set_xticklabels(model_names, rotation=45, ha='right')
    ax.set_ylabel("Mean Metric Value")
    ax.set_title("Cross-Validation Metrics for Each Model")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    plt.tight_layout()

    plot_path = os.path.join(results_folder, "validation_metrics.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    return summary_df

def plot_fold_roc_prc_curves(cv_results, results_folder="results"):
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    best_roc_model = max(cv_results, key=lambda m: cv_results[m]["mean_metrics"].get("roc_auc_cv_mean", -np.inf))
    best_trial = max(
        cv_results[best_roc_model]["all_trial_details"],
        key=lambda t: np.mean([fd["metrics"]["roc_auc"] for fd in t["fold_details"]])
    )

    fold_details = best_trial["fold_details"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    cmap = plt.cm.get_cmap("tab10", len(fold_details))

    for i, fd in enumerate(fold_details):
        y_true = fd["y_true_val"]
        y_prob = fd["y_prob_val"]

        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc_val = auc(fpr, tpr)
        ax1.plot(fpr, tpr, label=f"Fold {i} (AUC={roc_auc_val:.3f})", lw=1.5, alpha=0.8, color=cmap(i))

        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        prc_auc = auc(recall, precision)
        ax2.plot(recall, precision, label=f"Fold {i} (AP={prc_auc:.3f})", lw=1.5, alpha=0.8, color=cmap(i))

    ax1.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.7, label="Random")
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_xlabel("False Positive Rate")
    ax1.set_ylabel("True Positive Rate")
    ax1.set_title(f"ROC Curves (Best Model: {best_roc_model})")
    ax1.legend(loc="lower right")
    ax1.grid(True, ls="--", alpha=0.6)

    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel("Recall")
    ax2.set_ylabel("Precision")
    ax2.set_title(f"PRC Curves (Best Model: {best_roc_model})")
    ax2.legend(loc="lower left")
    ax2.grid(True, ls="--", alpha=0.6)

    plt.tight_layout()
    out_path = os.path.join(results_folder, "fold_roc_prc_curves.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[INFO] ROC & PRC curves for each fold saved to {out_path}.")

def report_best_model_parameters(cv_results, results_folder="results"):
    """
    Selects the overall best model based on ROC-AUC and writes its parameters to a text file.

    Parameters:
      cv_results (dict): Dictionary containing cross-validation results.
      results_folder (str): Folder to save the text file.

    Returns:
      tuple: (best_model_name, best_params)
    """
    best_model_name = max(cv_results, key=lambda m: cv_results[m]["mean_metrics"].get("roc_auc_cv_mean", -np.inf))
    best_params = cv_results[best_model_name]["best_params"]

    report_str = f"Best Model: {best_model_name}\nParameters:\n"
    for param, value in best_params.items():
        report_str += f"  {param}: {value}\n"

    output_path = os.path.join(results_folder, "best_model_parameters.txt")
    with open(output_path, "w") as f:
        f.write(report_str)

    return best_model_name, best_params
