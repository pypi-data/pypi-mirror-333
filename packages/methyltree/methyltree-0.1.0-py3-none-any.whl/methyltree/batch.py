import warnings

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from . import QC, metadata
from .settings import *

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None  # disable the SettingWithCopyWarning

####################################################

## This is meant for acc correction. No longer used

#####################################################


def order_by_FACS_sorting(df_sample):
    """
    Invert on the odd row, as in FACS
    """
    count = 0
    my_list = []
    for j, y in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
        temp = []
        for x in range(1, 13):
            temp.append(f"{y}{x}")
        if j % 2 == 0:
            my_list += temp
        else:
            my_list += list(np.array(temp)[::-1])
    df_tmp = pd.DataFrame({"FACS_order": my_list})
    df_sample["FACS_order"] = df_sample["sample"].apply(lambda x: x.split("_")[-1])
    return df_tmp.merge(df_sample, on="FACS_order")


def transform_rate(x, t1_over_t0, scale=1):
    """
    x is the input rate
    """
    offset = 10 ** (-10)
    if scale == 100:
        x = x / 100
        y = 1 - np.exp(-t1_over_t0 * np.log((1 + offset) / (1 + offset - x)))
        y = 100 * y
    else:
        y = 1 - np.exp(-t1_over_t0 * np.log((1 + offset) / (1 + offset - x)))

    return y


def estimate_t1_over_t0(global_rate_t0, global_rate_t1, scale=1):
    if scale == 100:
        global_rate_t0 = global_rate_t0 / 100
        global_rate_t1 = global_rate_t1 / 100

    t1_over_t0 = np.log(1.0001 - global_rate_t1) / np.log(1.0001 - global_rate_t0)
    return t1_over_t0


def QC_check_batch_correction(df_data, sample_1, sample_2, data_des=""):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    df_1 = df_data[df_data["sample"].isin([sample_1])]
    df_2 = df_data[df_data["sample"].isin([sample_2])]
    ax = sns.histplot(
        data=df_1, x="rate", label=sample_1, color="r", alpha=0.5, ax=axs[0]
    )
    ax = sns.histplot(
        data=df_2, x="rate", label=sample_2, color="b", alpha=0.5, ax=axs[0]
    )
    ax.legend()
    ax.set_title(f"Before correction: {data_des}")

    df_1 = df_data[df_data["sample"].isin([sample_1])]
    df_2 = df_data[df_data["sample"].isin([sample_2])]
    t1_over_t0 = estimate_t1_over_t0(
        df_2["rate"].mean(), df_1["rate"].mean(), scale=100
    )
    df_2["rate"] = df_2["rate"].apply(
        lambda x: transform_rate(x, t1_over_t0, scale=100)
    )
    sns.histplot(data=df_1, x="rate", label=sample_1, color="r", alpha=0.5, ax=axs[1])
    ax = sns.histplot(
        data=df_2, x="rate", label=sample_2, color="b", alpha=0.5, ax=axs[1]
    )
    ax.set_title(f"After correction: {data_des}")


def batch_correction_context_specific(df_input, df_sample, force_run=False):
    if (
        ("rate_before_correction" in df_input.columns)
        and ("t1_over_t0" in df_input.columns)
    ) and (not force_run):
        print("It seems that transformation has already been done. Abort")

    else:
        df_data = df_input.copy()
        df_data["rate_before_correction"] = df_data["rate"]
        df_data = df_data.merge(
            df_sample.filter(["sample", "lineage", "HQ"]), on="sample"
        )
        df_data = df_data[df_data["HQ"]]
        # obtain site-specific t1_over_t0 parameter
        df_tmp = (
            df_data.groupby(["sample", "anno", "lineage"])
            .agg(global_rate=("rate", "mean"))
            .reset_index()
        )
        df_tmp_2 = (
            df_data.groupby(["lineage", "anno"])
            .agg(lineage_rate=("rate", "mean"))
            .reset_index()
        )
        df_tmp = df_tmp.merge(df_tmp_2, on=["lineage", "anno"])
        anno_list = list(set(df_data["anno"]))
        df_tmp_list = []
        for anno in anno_list:
            df_anno = df_tmp[df_tmp["anno"] == anno]
            df_anno["t1_over_t0"] = estimate_t1_over_t0(
                df_anno["global_rate"], df_anno["lineage_rate"], scale=100
            )
            df_tmp_list.append(df_anno)
        df_tmp_new = pd.concat(df_tmp_list)
        df_data = df_data.merge(
            df_tmp_new.filter(
                ["sample", "anno", "global_rate", "lineage_rate", "t1_over_t0"]
            ),
            on=["sample", "anno"],
        )

        # perform transformation
        df_data["rate"] = transform_rate(
            df_data["rate"], df_data["t1_over_t0"], scale=100
        )

    return df_data


def batch_correction_global_time(df_input, df_sample, force_run=False, source="acc"):
    if ("rate_before_correction" in df_input.columns) and (not force_run):
        print("It seems that transformation has already been done. Abort")

    else:
        df_data = df_input.copy()
        df_data["rate_before_correction"] = df_data["rate"]
        df_sample_tmp = df_sample.copy()
        df_sample_tmp["rate_ref"] = 100 * df_sample_tmp[f"{source}_rate"]

        # obtain site-specific t1_over_t0 parameter
        df_tmp_2 = (
            df_sample_tmp[df_sample_tmp["HQ"]]
            .groupby(["lineage"])
            .agg(lineage_rate=("rate_ref", "mean"))
            .reset_index()
        )
        df_tmp = df_sample_tmp.filter(["lineage", "rate_ref", "sample", "HQ"]).merge(
            df_tmp_2, on=["lineage"]
        )
        # df_tmp["lineage_rate"] = 40
        # print("fix linenage rate to be constant")

        df_tmp["t1_over_t0"] = estimate_t1_over_t0(
            df_tmp["rate_ref"], df_tmp["lineage_rate"], scale=100
        )
        df_data = df_data.merge(df_tmp, on=["sample"])

        # perform transformation
        df_data["rate"] = transform_rate(
            df_data["rate"], df_data["t1_over_t0"], scale=100
        )
        df_data = df_data[df_data["HQ"]].drop("HQ", axis=1)
    return df_data


def log_transform(x, scale=100):
    if scale == 100:
        return np.log2(((x / 100) + 0.01) / (1 - (x / 100) + 0.01))
    else:
        return np.log2(((x) + 0.01) / (1 - (x) + 0.01))


def compare_global_rate_after_correction(df_data, N_thresh=1):
    df_data_tmp = df_data[df_data["N"] > N_thresh]
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    ax = sns.boxplot(
        data=df_data_tmp.groupby(["sample", "lineage"])
        .agg(rate=("rate_before_correction", "mean"))
        .reset_index(),
        x="lineage",
        y="rate",
        ax=axs[0],
    )
    ax.figure.autofmt_xdate(rotation=90)
    ax.set_ylabel("Global acc rate (before)")
    ax.set_xlabel("")

    ax = sns.boxplot(
        data=df_data_tmp.groupby(["sample", "lineage"])
        .agg(rate=("rate", "mean"))
        .reset_index(),
        x="lineage",
        y="rate",
        ax=axs[1],
    )
    ax.figure.autofmt_xdate(rotation=90)
    ax.set_ylabel("Global acc rate (after)")
    ax.set_xlabel("")
    title = "_".join(list(set(df_data_tmp["anno"]))) + f"; N_thresh={N_thresh}"
    fig.suptitle(title)


def compare_element_rate_after_correction(
    df_data, N_thresh=50, SampleList=None, lineage_rate_key="rate_ref"
):
    df_data_tmp = df_data[df_data["N"] > N_thresh]
    flag = 0
    if SampleList is None:
        flag = 1
        df_tmp = (
            df_data_tmp.groupby(["sample", "lineage"])
            .agg({lineage_rate_key: "mean"})
            .reset_index()
        )
        sel_lineage = (
            df_tmp.groupby("lineage")
            .agg(mean=(lineage_rate_key, "mean"), std=(lineage_rate_key, "std"))["std"]
            .idxmax()
        )
        df_tmp = (
            df_tmp[df_tmp["lineage"] == sel_lineage]
            .set_index("sample")
            .sort_values(lineage_rate_key)
            .reset_index()
        )

        max_sp = df_tmp["sample"].iloc[0]
        min_sp = df_tmp["sample"].iloc[-1]
        mean_sp = df_tmp["sample"].iloc[int(len(df_tmp) / 2)]
        SampleList = [max_sp, min_sp, mean_sp]

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    sns.histplot(
        data=df_data_tmp[df_data_tmp["sample"].isin(SampleList)],
        x="rate_before_correction",
        hue="sample",
        ax=axs[0],
    )
    sns.histplot(
        data=df_data_tmp[df_data_tmp["sample"].isin(SampleList)],
        x="rate",
        hue="sample",
        ax=axs[1],
    )
    title = "_".join(list(set(df_data_tmp["anno"]))) + f"; N_thresh={N_thresh}"
    if flag == 1:
        fig.suptitle(f"{sel_lineage}; " + title)
    else:
        fig.suptitle(title)
    plt.tight_layout()


##############################################

## Correlation metrics

##############################################


def compute_cell_cell_correlation(adata, lineage1, lineage2, nCG_thresh=10**6):
    from scipy.stats import pearsonr

    condition_1 = (adata.obs["lineage"] == lineage1) & (adata.obs["nGC"] > nCG_thresh)
    condition_2 = (adata.obs["lineage"] == lineage2) & (adata.obs["nGC"] > nCG_thresh)

    adata_tmp_1 = adata[condition_1]
    adata_tmp_2 = adata[condition_2]
    corr_list = []
    p_value_list = []
    cell_id_list = []
    for x in range(adata_tmp_1.shape[0]):
        X1 = adata_tmp_1.X[x, :].toarray()
        cell_id_1 = adata_tmp_1.obs_names[x]
        for y in range(1, adata_tmp_2.shape[0]):
            X2 = adata_tmp_2.X[y, :].toarray()
            cell_id_2 = adata_tmp_2.obs_names[y]
            sp_idx = (X1 > 0) & (X2 > 0)
            corr, pvalue = pearsonr(X1, X2)
            corr_list.append(corr)
            p_value_list.append(pvalue)
            cell_id_list.append((cell_id_1, cell_id_2))

    p_value_list = np.array(p_value_list)
    df_corr = pd.DataFrame(
        {"corr": corr_list, "pvalue": p_value_list, "sample": cell_id_list}
    )
    df_corr["logPvalue"] = -np.log(df_corr["pvalue"] + 10 ** (-10))
    df_corr = df_corr[df_corr["corr"] < 0.99]
    return df_corr


def compute_all_cell_cell_corr(adata, nCG_thresh=2 * 10**6):
    lineage_list = list(set(adata.obs["lineage"]))
    df_list = []
    pair_data = []
    count = 0
    for k in range(len(lineage_list)):
        count = count + 1
        lg1 = lineage_list[k]
        lg2 = lineage_list[k]
        df_corr = compute_cell_cell_correlation(adata, lg1, lg2, nCG_thresh=nCG_thresh)
        # pair_data.append((lg1,lg2))
        df_corr["lineage_pair"] = f"{lg1},{lg2}"
        df_corr["rank"] = count
        df_list.append(df_corr)

    for k in range(len(lineage_list)):
        for j in range(k, len(lineage_list)):
            lg1 = lineage_list[k]
            lg2 = lineage_list[j]
            df_corr = compute_cell_cell_correlation(
                adata, lg1, lg2, nCG_thresh=nCG_thresh
            )
            # pair_data.append((lg1,lg2))
            if lg1 != lg2:
                count = count + 1
                df_corr["lineage_pair"] = f"{lg1},{lg2}"
                df_list.append(df_corr)
                df_corr["rank"] = count

    df_final = pd.concat(df_list)

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.boxplot(data=df_final, x="lineage_pair", y="corr", ax=ax)
    plt.xlabel("")
    plt.xticks(rotation=90)
    plt.ylabel("Cell-cell corr across DNA elements")

    return df_final


def compare_plate_effect_after_batch_correction(df, df_sample, transform=False):
    """
    df should be output from batch correction method:
    batch_correction_global_time
    """
    df = df.merge(
        df_sample.filter(["id_acc", "id_met", "id_rna", "lineage", "sample"]),
        on="sample",
    )

    if transform:
        df["m_orig"] = log_transform(df["rate_before_correction"])
        df["m"] = log_transform(df["rate"])

        df_plot = (
            df.groupby(["sample", "lineage"])
            .agg(mean_rate=("m_orig", "mean"))
            .reset_index()
            .sort_values("sample")
            .reset_index()
        )
        g = sns.relplot(
            kind="scatter", data=df_plot, x="index", y="mean_rate", hue="lineage"
        )
        g.ax.set_xlabel("Ordered sample id")
        g.ax.set_ylabel("Original transformed rate")

        df_plot = (
            df.groupby(["sample", "lineage"])
            .agg(mean_rate=("m", "mean"))
            .reset_index()
            .sort_values("sample")
            .reset_index()
        )
        g = sns.relplot(
            kind="scatter", data=df_plot, x="index", y="mean_rate", hue="lineage"
        )
        g.ax.set_xlabel("Ordered sample id")
        g.ax.set_ylabel("Corrected transformed rate")
    else:
        df_plot = (
            df.groupby(["sample", "lineage"])
            .agg(mean_rate=("rate_before_correction", "mean"))
            .reset_index()
            .sort_values("sample")
            .reset_index()
        )
        g = sns.relplot(
            kind="scatter", data=df_plot, x="index", y="mean_rate", hue="lineage"
        )
        g.ax.set_xlabel("Ordered sample id")
        g.ax.set_ylabel("Original rate")

        df_plot = (
            df.groupby(["sample", "lineage"])
            .agg(mean_rate=("rate", "mean"))
            .reset_index()
            .sort_values("sample")
            .reset_index()
        )
        g = sns.relplot(
            kind="scatter", data=df_plot, x="index", y="mean_rate", hue="lineage"
        )
        g.ax.set_xlabel("Ordered sample id")
        g.ax.set_ylabel("Corrected rate")


def generate_count_matrix(
    root_dir, anno, source="acc", batch_correction="lineage", min_obs_N=3
):
    df_sample = metadata.load_sample_info(root_dir)
    if source == "acc":
        print("load acc")
        df_data = metadata.load_acc(root_dir, anno)
    else:
        print("load met")
        df_data = metadata.load_met(root_dir, anno)

    plt.hist(np.log10(1 + df_data["N"]), bins=100)
    plt.title("N counts histogram for raw data")

    # select high-quality cells, and genomic locus with high coverage
    df_sample["HQ"] = df_sample["HQ"] & (df_sample["acc_rate"] > 0.1)
    df_data = df_data[
        (df_data[f"N"] >= min_obs_N)
        & df_data["sample"].isin(df_sample[df_sample["HQ"]]["sample"])
    ]  # & (df_data['lineage']=='HSC') ]

    if batch_correction == "lineage":
        print("lineage specific batch correction")
        df_data = QC.batch_correction_context_specific(
            df_data, df_sample, force_run=False
        )
        QC.compare_global_rate_after_correction(df_data, N_thresh=1)
    elif batch_correction == "global":
        print("global batch correction")
        df_data = QC.batch_correction_global_time(df_data, df_sample, source=source)
        QC.compare_global_rate_after_correction(df_data, N_thresh=1)
    else:
        print("no batch correction")

    df_counts_raw = df_data.pivot(index=["sample"], columns="id", values=f"rate")
    return df_counts_raw
