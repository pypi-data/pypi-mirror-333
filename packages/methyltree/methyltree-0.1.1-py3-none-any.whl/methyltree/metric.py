import os

import numpy as np
import ot
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from matplotlib import pyplot as plt

from . import lineage
from .settings import *


def lineage_accuracy_from_leaf_order(ordered_clone_array, remove_nan=True):
    """
    The input should be like this:
    ['nan', 'nan', 'nan', '37', 'nan', ...,'nan', 'nan', '37', '2', '2', '2']
    """

    ##remove_nan
    ordered_clone_array = np.array(ordered_clone_array)
    nonnan_idx = np.array(["nan" not in x for x in ordered_clone_array])
    if remove_nan:
        ordered_clone_array_new = ordered_clone_array[nonnan_idx]
    else:
        ordered_clone_array_new = ordered_clone_array

    if len(ordered_clone_array_new) == 0:
        print("no valid clone ids to compute accuracy")
        return pd.DataFrame(
            {
                "clone": ["nan"],
                "clone_size": ["nan"],
                "accuracy": ["nan"],
                "continuity": ["nan"],
                "entropy": ["nan"],
                "wassertein": ["nan"],
            }
        )

    ## compute df_accuracy
    clone_set = list(set(ordered_clone_array_new))
    clone_accuracy = []
    clone_size = []
    clone_max = []
    for x in clone_set:
        tot_N = np.sum(ordered_clone_array_new == x)
        clone_size.append(tot_N)
        continuous_sum = 0
        max_sum = 0
        for j in range(len(ordered_clone_array_new)):
            if ordered_clone_array_new[j] == x:
                continuous_sum = continuous_sum + 1
                if continuous_sum > max_sum:
                    max_sum = continuous_sum
            else:
                continuous_sum = 0
        if max_sum > 1:
            clone_accuracy.append(max_sum / tot_N)
        else:
            clone_accuracy.append(0)
        clone_max.append(max_sum)
    df_accuracy = pd.DataFrame(
        {"clone": clone_set, "clone_size": clone_size, "accuracy": clone_accuracy}
    )
    df_size = pd.DataFrame(
        {"clone": clone_set, "clone_size": clone_size, "clone_max": clone_max}
    )

    #### compute df_entropy
    counter = 0
    x0 = ordered_clone_array_new[0]
    class_list = [0]
    for x in ordered_clone_array_new[1:]:
        if x == x0:
            class_list.append(counter)
        else:
            counter += 1
            x0 = x
            class_list.append(counter)
    df = pd.DataFrame({"clone": ordered_clone_array_new, "class": class_list})
    df_1 = (
        df.groupby(["clone", "class"])
        .apply(lambda x: len(x))
        .reset_index()
        .rename(columns={0: "count"})
    )
    entropy_dict = {}
    for j, x in enumerate(df_1["clone"].unique()):
        df_sub = df_1[df_1["clone"] == x]
        size = df_sub["count"].sum()
        df_sub["prob"] = df_sub["count"] / size
        prob = df_sub["prob"].to_numpy()
        entropy_dict[x] = (np.sum(-prob * np.log(prob))) / np.log(size)
    df_entropy = pd.DataFrame(
        {"clone": entropy_dict.keys(), "entropy": entropy_dict.values()}
    )

    ### compute df_block
    df_block = df_1[["clone"]]
    df_block["block_count"] = df_block.groupby("clone")["clone"].transform("count")
    df_block = df_block.drop_duplicates("clone")
    df_block = df_block.merge(df_size, on="clone")
    df_block["continuity"] = 1 - (df_block["block_count"] - 1) / df_block["clone_size"]
    # print(df_block)
    df_block = df_block[["clone", "continuity"]]

    ### compute df_wassertein
    clone_vector_list = []
    reference_vector_list = []
    Wassertein_list = []
    for clone in clone_set:
        total_clone_length = len(ordered_clone_array_new)
        clone_vector_list = (
            (ordered_clone_array_new == clone).astype(int)
        ).tolist()  # constructing a list of resulting clones
        clone_length = sum(clone_vector_list)  # need to be clone specific

        cover_num = 0
        for p in range(total_clone_length - int(clone_length) + 1):
            new_cover_num = sum(clone_vector_list[p : p + int(clone_length)])
            if cover_num < new_cover_num:
                cover_num = new_cover_num
                ref_start = p
        # constructing a list of reference clones
        reference_vector_list = [
            1 if ref_start <= n < ref_start + int(clone_length) else 0
            for n in range(total_clone_length)
        ]
        input_t0 = np.array(clone_vector_list).astype(float)
        input_t1 = np.array(reference_vector_list).astype(float)

        M = np.where(np.eye(len(input_t0)), 0, 1).astype(int)
        Wd = ot.emd2(
            input_t0, input_t1, M
        )  # compute the Wassterin distance between the observed clone vector and the reference vector
        Wassertein_list.append(Wd / clone_length)
    df_wass = pd.DataFrame({"clone": clone_set, "wassertein": Wassertein_list})

    ### merge results
    df_result = (
        df_accuracy.merge(df_block, on="clone")
        .merge(df_entropy, on="clone")
        .merge(df_wass, on="clone")
        .sort_values(by="clone")
    )
    return df_result[df_result["clone_size"] > 1].filter(
        ["clone", "clone_size", "accuracy", "continuity", "entropy", "wassertein"]
    )


def compute_accuracy_by_depth(
    my_tree, orig_clone_order, method="mean", accuracy_key="continuity"
):
    curr_list = [my_tree]
    depth_count = 0
    accuracy_list = []

    while len(curr_list) > 0:
        next_list = []
        for t in curr_list:
            order_x = np.array(t.get_leaf_names()).astype(int)
            ordered_clone_array = np.array(orig_clone_order).astype(str)[order_x]
            if list(set(ordered_clone_array)) != ["nan"]:
                df_accuracy = lineage_accuracy_from_leaf_order(ordered_clone_array)
                # df_accuracy = df_accuracy[df_accuracy["clone_size"] > 1]
                if len(df_accuracy) > 0:
                    # display(df_1)
                    if method == "mean":
                        mean_accu = df_accuracy[accuracy_key].mean()
                    else:
                        mean_accu = np.sum(
                            df_accuracy[accuracy_key]
                            * df_accuracy["clone_size"]
                            / df_accuracy["clone_size"].sum()
                        )
                    accuracy_list.append(
                        [
                            depth_count,
                            "@".join(df_accuracy["clone"]),
                            df_accuracy["clone_size"].sum(),
                            mean_accu,
                        ]
                    )

            if not t.is_leaf():
                next_list += t.children

        depth_count += 1
        curr_list = next_list
    df = pd.DataFrame(
        accuracy_list, columns=["Depth", "clone", "total_cell_N", accuracy_key]
    )
    return df


def get_accuracy_report(
    out_dir, groupby="lineage", clone_key=None, accuracy_key="accuracy"
):
    """
    groupby can be: 'lineage','patient'
    """

    if clone_key is not None:
        groupby = clone_key + "_" + groupby

    data_des = f"accuracy_{groupby}_"
    all_files = [x for x in os.listdir(out_dir) if x.startswith(data_des)]
    mean_accuracy = []
    weighted_accuracy = []
    tot_clones = []
    for x in all_files:
        df = pd.read_csv(f"{out_dir}/{x}")
        df = df[df["clone_size"] > 1]
        tot_clones.append(len(df))
        weighted_accuracy_tmp = np.sum(
            df[accuracy_key] * df["clone_size"] / df["clone_size"].sum()
        )
        mean_accuracy_tmp = df[accuracy_key].mean()

        mean_accuracy.append(mean_accuracy_tmp)
        weighted_accuracy.append(weighted_accuracy_tmp)

    df_accuracy = pd.DataFrame(
        {
            "FileName": all_files,
            "Total_clone": tot_clones,
            f"mean_{accuracy_key}": mean_accuracy,
            f"weighted_{accuracy_key}": weighted_accuracy,
        }
    )
    df_accuracy["Metadata"] = df_accuracy["FileName"].apply(
        lambda x: x.split(data_des)[1].split("_readcutoff3_minCov")[0]
    )
    for z in ["readcutoff", "minCov", "ExcludeSex"]:
        df_accuracy[z] = df_accuracy["FileName"].apply(
            lambda x: x.split(z)[1].split("_")[0] if z in x else None
        )
    df_accuracy["Stage"] = df_accuracy["Metadata"].apply(lambda x: x.split("_")[0])
    df_accuracy["Annotation"] = df_accuracy["Metadata"].apply(
        lambda x: "_".join(x.split("_")[1:])
    )
    df_accuracy["Source"] = df_accuracy["FileName"].apply(
        lambda x: x.split("_minCov")[1].split("_")[1]
    )

    sel_columns = [
        "Stage",
        "Source",
        "Annotation",
        "readcutoff",
        "minCov",
        "ExcludeSex",
        "Total_clone",
        f"mean_{accuracy_key}",
        f"weighted_{accuracy_key}",
    ]
    df_accuracy = df_accuracy.filter(sel_columns).sort_values(["Stage", "Annotation"])
    for z in ["Source", "ExcludeSex"]:
        df_accuracy[z] = df_accuracy[z].apply(
            lambda x: x.split(".csv")[0] if ((x is not None) and (".csv" in x)) else x
        )
    return df_accuracy


def accuracy_at_different_similarity_threshold(
    X_similarity, my_tree, clone_array, accuracy_key="continuity"
):
    clone_array = np.array(clone_array).astype(str)
    unique_clone_set = list(set(clone_array))
    for x0 in unique_clone_set:
        if np.sum(clone_array == x0) == 1:
            clone_array[clone_array == x0] = "nan"

    ################## Actually identify clones
    lineage.traverse_tree_to_update_dist(my_tree, X_similarity, method="mean")
    S_array = []
    for tmp_tree in my_tree.traverse():
        S_array.append(tmp_tree.dist)
    S_array = np.array(S_array)
    S_array = S_array[~np.isnan(S_array)]

    plt.subplots(figsize=(4, 3.5))
    sns.histplot(S_array, bins=20)
    plt.xlabel("Similarity at branches")
    plt.ylabel("Count")

    mean_accuracy = []
    mean_entropy = []
    relative_cell_fraction = []
    used_threshold_list = []
    step = (np.max(S_array) - np.min(S_array)) / 20
    weight_threshold_list = np.arange(np.min(S_array), np.max(S_array), step)
    for weight_threshold in weight_threshold_list:

        def traverse_tree(node, weight):
            if node.dist >= weight:
                # print(node)
                leaf_idx = np.array(node.get_leaf_names()).astype(int)
                unique_clone_set_tmp = list(set(clone_array[leaf_idx]))
                if unique_clone_set_tmp != ["nan"]:
                    df_tmp = pd.DataFrame({"cell_id": leaf_idx})
                    df_tmp["predicted_clone"] = f"clone_{len(df_list)}"
                    df_tmp["clone_weight"] = node.dist
                    df_tmp["clone_size"] = len(leaf_idx)

                    df_list.append(df_tmp)

            else:
                for child in node.children:
                    traverse_tree(child, weight)

        df_list = []
        traverse_tree(my_tree, weight_threshold)
        if len(df_list) > 0:
            df_result = pd.concat(df_list)
            cell_idx = df_result["cell_id"].to_numpy()
            df_accuracy = lineage_accuracy_from_leaf_order(clone_array[cell_idx])
            mean_accuracy.append(df_accuracy[accuracy_key].mean())
            relative_cell_fraction.append(len(df_result) / len(clone_array))
            used_threshold_list.append(weight_threshold)
    df_final = pd.DataFrame(
        {
            "weight_threshold": used_threshold_list,
            accuracy_key: mean_accuracy,
            "cell_fraction": relative_cell_fraction,
        }
    )
    df_final = (
        df_final.groupby("cell_fraction")
        .agg(
            {
                "weight_threshold": "mean",
                accuracy_key: "mean",
            }
        )
        .reset_index()
        .sort_values("cell_fraction")
    )

    # compute AUC score
    cell_fraction_array = [0] + list(df_final["cell_fraction"])
    accuracy_list = list(df_final[accuracy_key])
    accuracy_array = np.array([accuracy_list[0]] + list(accuracy_list))
    accuracy_array = (accuracy_array[:-1] + accuracy_array[1:]) / 2
    AUC = np.sum(accuracy_array * np.diff(cell_fraction_array))

    # plot
    plt.subplots(figsize=(4, 3.5))
    plt.plot(df_final["weight_threshold"], df_final[accuracy_key], "-*r")
    plt.title(f"{AUC:.4f}")
    plt.xlabel("Similarity threshold")
    plt.ylabel(f"Mean {accuracy_key}")
    plt.xlim([0, 1.02])
    plt.ylim([0, 1.02])
    return df_final


def accuracy_after_removing_leaves_with_low_support(
    df_predict, adata, clone_key, accuracy_key="continuity"
):
    """
    accuracy after filtering out unreliable cells with low tree support
    """
    df_predict["cell_id_new"] = np.array(
        df_predict["cell_id"].apply(lambda x: x.split("-")[0])
    ).astype(int)
    df_predict["predict_large_clone"] = df_predict["clone_size"] > 1
    adata.obs["predicted_large_clone"] = df_predict.sort_values("cell_id_new")[
        "predict_large_clone"
    ].to_numpy()
    sel_idx = ~adata.obs[
        "predicted_large_clone"
    ]  # pd.isna(adata.obs["inferred_clones"])
    old_clone_array = adata.obs[clone_key].copy().to_numpy()
    old_clone_array[sel_idx] = np.nan
    # switch to new clone_key
    ordered_clone_array = old_clone_array[adata.uns["order_x"]].astype(str)
    df_accuracy = lineage_accuracy_from_leaf_order(ordered_clone_array)
    mean_accuracy = df_accuracy[accuracy_key].mean()
    print(
        f"Remaining cell fraction: {np.mean(~sel_idx):.2f};\nClone_N: {len(df_accuracy)};\nMean {accuracy_key}: {mean_accuracy:.2f}; "
    )


def methy_clone_diversity_index(df_predict):
    df_predict["barcode"] = df_predict["cell_id"].apply(lambda x: x.split("-")[-1])

    def observed_clone_size(x):
        x = np.array(x)
        return len(x[x != "nan"])

    def concatenate_clone(x):
        x = list(set(x))
        if "nan" in x:
            x.remove("nan")
        return "_".join(x)

    def barcode_count(x):
        x = list(set(x))
        if "nan" in x:
            x.remove("nan")
        return len(x)

    df_clone_info = df_predict.groupby(["predicted_clone"]).agg(
        barcode_clone_size=("barcode", observed_clone_size),
        barcode_list=("barcode", concatenate_clone),
        barcode_count=("barcode", barcode_count),
    )
    valid_methy_clones = len(
        df_clone_info[
            (df_clone_info["barcode_clone_size"] > 1)
            & (df_clone_info["barcode_count"] == 1)
        ]["barcode_list"].unique()
    )
    merged_methy_clones = np.sum(df_clone_info["barcode_count"] > 1)
    # print(f"Methy clone diversity score: {methy_clone_diversity}")
    return df_clone_info, valid_methy_clones, merged_methy_clones


#####################################

# correlation between met and rna etc

#####################################


def compute_correlation(
    df_data,
    key_1="acc",
    key_2="met",
    corr_by="id",
    cutoff_met_N=2,
    cutoff_acc_N=2,
    mini_size=20,
    save=None,
):
    key_map = {"acc": "acc_rate", "met": "met_rate", "rna": "rna_exp"}
    actual_key_1 = key_map[key_1]
    actual_key_2 = key_map[key_2]
    keep_keys = [
        actual_key_1,
        actual_key_2,
        f"pass_{key_1}QC",
        f"pass_{key_2}QC",
        corr_by,
    ]
    if "met" in [key_1, key_2]:
        keep_keys.append("met_N")
    if "acc" in [key_1, key_2]:
        keep_keys.append("acc_N")

    df_sub = df_data.filter(keep_keys).dropna()
    custom_filter = df_sub[f"pass_{key_1}QC"] & df_sub[f"pass_{key_1}QC"]
    if "met" in [key_1, key_2]:
        keep_keys.append("met_N")
        custom_filter = custom_filter & (df_sub["met_N"] > cutoff_met_N)
    if "acc" in [key_1, key_2]:
        keep_keys.append("acc_N")
        custom_filter = custom_filter & (df_sub["acc_N"] > cutoff_acc_N)

    # series=df_sub[custom_filter].groupby(corr_by).apply(lambda x: np.corrcoef(x[actual_key_1],x[actual_key_2])[0,1])
    df_out = (
        df_sub[custom_filter]
        .groupby(corr_by)
        .apply(
            lambda x: (
                stats.pearsonr(x[actual_key_1], x[actual_key_2])
                if len(x) > mini_size
                else (np.nan, np.nan)
            )
        )
    )
    df_final = (
        pd.DataFrame(df_out.to_list(), index=df_out.index)
        .rename(columns={0: "Corr", 1: "Pvalue"})
        .dropna()
        .assign(log10Pvalue=lambda x: -np.log10(x["Pvalue"]))
    )

    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    ax = sns.histplot(data=df_final, x="Corr", bins=20, ax=axs[0])
    ax.set_xlabel(f"Corr: {key_1}-{key_2}")
    ax.set_ylabel(f"Histogram")
    ax.set_title(f"Mean: {df_final.Corr.mean():.3f}")
    ax = sns.histplot(data=df_final, x="Corr", y="log10Pvalue", bins=30, ax=axs[1])
    ax.set_xlabel(f"Corr: {key_1}-{key_2}")
    ax.set_ylabel(f"-log10Pvalue")
    ax.set_title(f"Correlation by {corr_by}")
    ax = sns.scatterplot(data=df_final, x="Corr", y="log10Pvalue", ax=axs[2], s=10)
    ax.set_xlabel(f"Corr: {key_1}-{key_2}")
    ax.set_ylabel(f"-log10Pvalue")
    ax.set_title(f"Correlation by {corr_by}")
    fig.tight_layout()
    if save is not None:
        fig.savefig(save)

    return df_final


def compute_coarse_grained_correlation(
    df_data,
    key_1="acc",
    key_2="met",
    corr_by="id",
    coarse_grained_by="celltype",
    mini_size=1,
):
    key_map = {"acc": "acc_rate", "met": "met_rate", "rna": "rna_exp"}
    actual_key_1 = key_map[key_1]
    actual_key_2 = key_map[key_2]
    custom_filter = df_data[f"pass_{key_1}QC"] & df_data[f"pass_{key_1}QC"]
    df_metaccrna_v1 = (
        df_data[custom_filter]
        .groupby(["id", coarse_grained_by, "anno"])
        .agg(
            acc_rate=("acc_rate", "mean"),
            met_rate=("met_rate", "mean"),
            rna_exp=("rna_exp", "mean"),
        )
        .reset_index()
    )

    # coarse-grain by counting all the met sites and unmet sites does not work as well, suggsting strong batch difference across cells
    # df_metaccrna_v1=df_data[custom_filter].groupby(['id',coarse_grained_by,'anno']).agg(met_Nmet=('met_Nmet','sum'),met_N=('met_N','sum'),
    #     acc_Nmet=('acc_Nmet','sum'),acc_N=('acc_N','sum'),rna_exp=('rna_exp','mean')).reset_index().assign(met_rate=lambda df: df['met_Nmet']/df['met_N']).assign(acc_rate=lambda df: df['acc_Nmet']/df['acc_N'])

    df_out = df_metaccrna_v1.groupby("id").apply(
        lambda x: (
            stats.pearsonr(x[actual_key_1], x[actual_key_2])
            if len(x) > 3
            else (np.nan, np.nan)
        )
    )

    df_final = (
        pd.DataFrame(df_out.to_list(), index=df_out.index)
        .rename(columns={0: "Corr", 1: "Pvalue"})
        .dropna()
        .assign(log10Pvalue=lambda x: -np.log10(x["Pvalue"]))
    )

    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    ax = sns.histplot(data=df_final, x="Corr", bins=20, ax=axs[0])
    ax.set_xlabel(f"Corr: {key_1}-{key_2}")
    ax.set_ylabel(f"Histogram")
    ax.set_title(f"Mean: {df_final.Corr.mean():.3f}")
    ax = sns.histplot(data=df_final, x="Corr", y="log10Pvalue", bins=30, ax=axs[1])
    ax.set_xlabel(f"Corr: {key_1}-{key_2}")
    ax.set_ylabel(f"-log10Pvalue")
    ax.set_title(f"Correlation by {corr_by}")
    ax = sns.scatterplot(data=df_final, x="Corr", y="log10Pvalue", ax=axs[2], s=10)
    ax.set_xlabel(f"Corr: {key_1}-{key_2}")
    ax.set_ylabel(f"-log10Pvalue")
    ax.set_title(f"Correlation by {corr_by}")
    plt.tight_layout()

    return df_final, df_metaccrna_v1
