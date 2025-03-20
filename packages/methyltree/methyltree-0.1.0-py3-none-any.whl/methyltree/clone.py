import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from ete3 import Tree
from matplotlib import pyplot as plt
from tqdm import tqdm

from . import lineage, metric
from .settings import *

#########################
# clone identification
#########################


def identify_putative_clones_from_trees_with_support(
    tree_path,
    X_similarity,
    support_threshold=0.6,
    print_clone=False,
    similarity_percentile=75,
    verbose=True,
    method="high",
    t_test_threshold_high=1.5,
    t_test_threshold_low=0.75,
    t_test_size_cutoff=3,
    p_value_threshold=0.05,
):
    """
    low: the original method, based on support value and similarity threshold. Seach starting from root.
    This method typically results in low clone resolution.

    high: on top of the low method, further explore whether the identified sub-tree can be furtehr partitioned into sub-clones. When the a sub-tree within the current node can be split into sub-clones, start from this sub-tree, and then
    also add other branches not leading towards this sub-tree.
    This method is currently our best method.

    t-test: on top of the low method, a combination of t-test and support value threshold method to further refine the sub-clones. In t-test, we test whether the current two branches under this node actually belong to two different clones.

    deep: on top of the low method, further search within the current clone for sub-trees that has the right support value. Different from the 'high' method, it does not require two branches under the same node to be valid sub-trees.
    This method tends to produce very small clones.

    shapiro: based on shapiro test
    """

    print(f"method {method}")
    available_methoes = ["high", "low", "t-test", "deep", "shapiro"]
    if method not in available_methoes:
        raise ValueError(f"method is {method}, but should be among {available_methoes}")
    with open(tree_path, "r") as f:
        my_tree = Tree(f.read(), support=True)
        my_tree.support = 0

    tree_list = []
    support = []
    df_list = []

    lineage.traverse_tree_to_update_dist(
        my_tree, X_similarity, percentile=50, rename_leaf_map=lambda x: x.split("-")[0]
    )
    mean_similarity = np.percentile(X_similarity.flatten(), similarity_percentile)

    ##########################
    ### supporting functions
    ##########################
    def collect_putative_clones(node_tmp):
        tree_list.append(node_tmp)
        leaf_idx = np.array(node_tmp.get_leaf_names())
        df_tmp = pd.DataFrame({"cell_id": leaf_idx})
        df_tmp["predicted_clone"] = f"clone_{len(df_list)}"
        df_tmp["clone_support"] = float(node_tmp.support)
        df_tmp["clone_weight"] = float(node_tmp.dist)
        df_tmp["clone_size"] = len(leaf_idx)
        df_list.append(df_tmp)
        if print_clone:  # and (len(leaf_idx)>1):
            renamed_node = node_tmp.copy()
            print(renamed_node)

    def collect_sub_tree_information(node_tmp, level=0, data_list=[], name="0"):
        valid_tmp = (
            (float(node_tmp.support) >= support_threshold)
            & (node_tmp.dist >= mean_similarity)
            & (~node_tmp.is_leaf())
        )
        data_list.append([level, int(valid_tmp), len(node_tmp.get_leaf_names()), name])
        for j0, child_tmp in enumerate(node_tmp.children):
            collect_sub_tree_information(
                child_tmp, level + 1, data_list=data_list, name=f"{name},{j0}"
            )

    def add_clone_info_from_target_level(
        node_tmp, target_level, target_name_list, level=0, name="0"
    ):
        valid_list = []
        invalid_list = []
        for target_name in target_name_list:
            # this sub-tree matches our target names
            condition_1 = target_name == name
            # this sub-tree is along the branch that leads to the target sub-tree, therefore acceptable
            condition_2 = target_name.startswith(name)
            # this sub-tree is contained within one of the target sub-trees
            condition_3 = name.startswith(target_name)
            valid_list.append(condition_1)
            invalid_list.append(condition_2 or condition_3)
        valid = np.sum(valid_list) > 0
        if not valid:
            valid = np.sum(invalid_list) == 0

        if valid:
            collect_putative_clones(node_tmp)
            if name not in target_name_list:
                target_name_list.append(name)

        # print(target_name_list)
        if level < target_level:
            for j0, child_tmp in enumerate(node_tmp.children):
                add_clone_info_from_target_level(
                    child_tmp,
                    target_level,
                    target_name_list,
                    level=level + 1,
                    name=f"{name},{j0}",
                )
        else:
            return

    def refine_clone_based_on_support_high_method(node):
        data_list = []
        collect_sub_tree_information(node, level=0, data_list=data_list)
        df_tmp_orig = pd.DataFrame(
            np.array(data_list), columns=["level", "score", "cell_N", "name"]
        )
        df_tmp_orig["level"] = df_tmp_orig["level"].astype(int)
        df_tmp_orig["score"] = df_tmp_orig["score"].astype(float)
        df_tmp_orig["cell_N"] = df_tmp_orig["cell_N"].astype(int)

        # print(df_tmp_orig)
        df_tmp = (
            df_tmp_orig.groupby("level")
            .agg({"score": "mean", "cell_N": "sum"})
            .reset_index()
        )
        df_tmp = df_tmp[(df_tmp["score"] == 1)]
        # print(df_tmp)
        target_level = df_tmp["level"].max()
        target_name_list = df_tmp_orig[df_tmp_orig["level"] == target_level][
            "name"
        ].to_list()
        add_clone_info_from_target_level(node, target_level, target_name_list)

    def support_value_status(node_tmp, support_threshold, mean_similarity):
        valid_list = []
        for child_tmp in node_tmp.children:
            valid_tmp = (
                (float(child_tmp.support) >= support_threshold)
                & (child_tmp.dist > mean_similarity)
                & (~child_tmp.is_leaf())
            )
            valid_list.append(valid_tmp)
        return np.mean(np.array(valid_list).astype(int)) > 0.999

    def refine_clones_based_on_t_test_and_support(node):

        def t_test_status(node, size_cutoff):
            # a size_cutoff to avoid splitting the clusters to be too small
            child_list = []
            for child in node.children:
                child_list.append(child)
            order_0 = np.array(
                [x.split("-")[0] for x in child_list[0].get_leaf_names()]
            ).astype(int)
            order_1 = np.array(
                [x.split("-")[0] for x in child_list[1].get_leaf_names()]
            ).astype(int)
            if (len(order_0) >= size_cutoff) & (len(order_1) >= size_cutoff):
                X_01 = X_similarity[order_0][:, order_1]
                X_0 = X_similarity[order_0][:, order_0]
                X_1 = X_similarity[order_1][:, order_1]
                tmp_intra = np.hstack(
                    (
                        X_0[np.triu_indices_from(X_0, k=1)],
                        X_1[np.triu_indices_from(X_1, k=1)],
                    )
                )  # [child_list[0].dist, child_list[1].dist]
                tmp_cross = X_01.flatten()

                return (
                    np.mean(tmp_intra) - tmp_cross.mean()
                ) / tmp_intra.std()  # tmp_cross.std()
            else:
                return None

        condition_1 = support_value_status(node, support_threshold, mean_similarity)
        t_test_value = t_test_status(node, t_test_size_cutoff)
        if t_test_value is not None:
            condition_2 = t_test_value > t_test_threshold_high
            condition_3 = t_test_value < t_test_threshold_low
        else:
            condition_2 = False  # not informative
            condition_3 = False  # do not affect whether to split clones or not

        print(
            f"T-test value: {t_test_value } condition {condition_1}   {condition_2} {condition_3}"
        )

        if (condition_1 or condition_2) and (not condition_3):
            for child in node.children:
                refine_clones_based_on_t_test_and_support(child)
        else:
            collect_putative_clones(node)

    def refine_clones_based_on_shapiro_test_and_support(node):
        def shapiro_test(node):
            order_x = np.array([x.split("-")[0] for x in node.get_leaf_names()]).astype(
                int
            )
            if len(order_x) >= t_test_size_cutoff:
                X = X_similarity[order_x][:, order_x]
                X_flat = X[np.triu_indices_from(X, k=1)].flatten()
                result = stats.shapiro(X_flat)
                return result.pvalue
            else:
                return None

        condition_1 = support_value_status(node, support_threshold, mean_similarity)
        p_value = shapiro_test(node)

        if p_value is not None:
            condition_2 = p_value < p_value_threshold
            if condition_2:
                print(f"p_value: {p_value}")
        else:
            condition_2 = False  # not informative

        if condition_1 or condition_2:
            for child in node.children:
                refine_clones_based_on_shapiro_test_and_support(child)
        else:
            collect_putative_clones(node)

    def refine_clones_based_on_support_deep_method(node):
        if (
            (float(node.support) >= support_threshold)
            & (node.dist > mean_similarity)
            & (~node.is_leaf())
        ):
            for child in node.children:
                refine_clones_based_on_support_deep_method(child)
        else:
            collect_putative_clones(node)

    def get_support_distribution(node):
        if not node.is_leaf():
            support.append(float(node.support))
        for child in node.children:
            get_support_distribution(child)

    def identify_clone_main(node):
        if node.is_leaf():
            collect_putative_clones(node)
        elif (
            (float(node.support) >= support_threshold)
            & (node.dist > mean_similarity)
            & (~node.is_leaf())
        ):
            # if print_clone:
            #     print(f'----------full-sub tree-----------')
            #     renamed_node = node.copy()
            #     print(renamed_node)
            #     print('******** collected tree *********')

            if method == "low":
                collect_putative_clones(node)
            elif method == "high":
                refine_clone_based_on_support_high_method(node)
            elif method == "t-test":
                refine_clones_based_on_t_test_and_support(node)
            elif method == "shapiro":
                refine_clones_based_on_shapiro_test_and_support(node)
            else:
                refine_clones_based_on_support_deep_method(node)

        else:
            for child in node.children:
                identify_clone_main(child)

    ###################################
    ####### Call these functions
    ###################################

    identify_clone_main(my_tree.copy())

    df_predict = pd.concat(df_list, ignore_index=True)

    ## rename clone id according to its size
    clone_key = "predicted_clone"
    df_tmp = (
        df_predict.groupby(clone_key)
        .agg({"clone_size": "mean"})
        .sort_values("clone_size", ascending=False)
        .reset_index()
        .reset_index()
    )
    df_tmp[f"new_{clone_key}"] = "clone_" + df_tmp["index"].astype(str)
    clone_key_map = dict(zip(df_tmp[clone_key], df_tmp[f"new_{clone_key}"]))
    df_predict[f"{clone_key}"] = df_predict[clone_key].map(clone_key_map)

    if verbose:
        get_support_distribution(my_tree.copy())
        plt.subplots()
        sns.histplot(support, binwidth=0.05)
        plt.xlabel("Support")
        plt.ylabel("Count")
        df_predict_tmp = df_predict[df_predict["clone_size"] > 1]
        print(
            "Total predicted clones (>1 cells)",
            len(df_predict_tmp["predicted_clone"].unique()),
        )

    return df_predict


def identify_putative_clones(
    X_similarity_old,
    my_tree,
    weight_threshold,
    plot_signal_noise=True,
    rename_leaf_map=None,
    print_clone=False,
):
    ########################################################
    # Signal-noise plot to decide the weight threshold to call clones
    ########################################################
    order_x = np.array(my_tree.get_leaf_names()).astype(int)
    X_similarity = X_similarity_old.copy()

    if plot_signal_noise:
        for i in range(X_similarity.shape[0]):
            X_similarity[i, i] = np.nan  # to avoid counting the diagonal terms

        # Obtain randomized similarity
        X_similarity_rand = X_similarity.copy()
        rand_dist = []
        cell_orders = np.arange(X_similarity.shape[0])
        for __ in tqdm(range(100)):
            np.random.shuffle(cell_orders)
            lineage.traverse_tree_to_update_dist(
                my_tree, X_similarity_rand[cell_orders][:, cell_orders], percentile=50
            )
            for tmp_tree in my_tree.traverse():
                rand_dist.append(tmp_tree.dist)

        # Obtain true similarity
        lineage.traverse_tree_to_update_dist(my_tree, X_similarity, percentile=50)
        true_dist = []
        for tmp_tree in my_tree.traverse():
            true_dist.append(tmp_tree.dist)

        rand_dist = np.array(rand_dist)
        rand_dist = rand_dist[~np.isnan(rand_dist)]
        true_dist = np.array(true_dist)
        true_dist = true_dist[~np.isnan(true_dist)]

        plt.subplots(1, 1, figsize=(5.5, 3.5))
        color_random = "#a6bddb"
        color_data = "#fdbb84"

        all_data = list(true_dist) + list(rand_dist)
        bins = np.linspace(np.min(all_data), np.max(all_data), 50)

        ax = sns.histplot(
            data=true_dist,
            label="Observed",
            bins=bins,
            stat="probability",
            color=color_data,
            alpha=0.5,
        )

        ax = sns.histplot(
            data=rand_dist,
            label="Random",
            bins=bins,
            stat="probability",
            color=color_random,
        )

        # ax.legend()
        plt.legend(loc=[1.05, 0.4])
        # ax.set_xlabel("Sister-cell distance")
        plt.xlabel("Tree weight")
        plt.ylabel("Normalized frequency")
        # plt.yscale('log')
        plt.tight_layout()

    ################## Actually identify clones
    lineage.traverse_tree_to_update_dist(my_tree, X_similarity, percentile=50)
    tree_list = []
    dist = []
    df_list = []

    def traverse_tree(node):
        dist.append(node.dist)
        if node.dist > weight_threshold:
            if print_clone and rename_leaf_map is not None:
                renamed_node = node.copy()
                for j, leaf in enumerate(renamed_node.iter_leaves()):
                    # Modify the leaf name based on your desired logic
                    new_name = f"{j}" + "; " + str(rename_leaf_map[leaf.name])
                    leaf.name = new_name
                print(renamed_node)

            tree_list.append(node)
            leaf_idx = np.array(node.get_leaf_names()).astype(int)
            df_tmp = pd.DataFrame({"cell_id": leaf_idx})
            df_tmp["predicted_clone"] = f"clone_{len(df_list)}"
            df_tmp["clone_weight"] = node.dist
            df_tmp["clone_size"] = len(leaf_idx)
            df_list.append(df_tmp)

        else:
            for child in node.children:
                traverse_tree(child)

    traverse_tree(my_tree.copy())
    # print("Total count", len(tree_list))

    df_predict = pd.concat(df_list, ignore_index=True)
    df = (
        pd.DataFrame({"cell_id": order_x})
        .merge(df_predict, on="cell_id", how="outer")
        .sort_values("cell_id")
        .reset_index(drop=True)
    )
    return df.sort_values("clone_weight", ascending=False)


def infer_clone_number_across_various_threshold(
    adata, out_dir, clone_key, save_data_des, fig_dir
):
    my_tree_path = f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}.txt"
    df_state_clone = pd.read_csv(
        f"{out_dir}/state_clone_info_{clone_key}_{save_data_des}.csv"
    )
    rename_leaf_map = dict(
        zip(df_state_clone["state_info"].astype(str), df_state_clone["clone_id"])
    )

    with open(my_tree_path, "r") as f:
        my_tree = Tree(f.read(), support=False)

    order_x = np.array(my_tree.get_leaf_names()).astype(int)

    used_threshold_list = []
    accuracy_list = []
    fraction_list = []
    obs_clone_N_list = []
    estimated_total_clone_N_list = []
    for infer_clone_threshold_tmp in np.arange(0.4, 0.9, 0.02):
        df_tmp = identify_putative_clones(
            adata.obsm["X_similarity"],
            my_tree.copy(),
            weight_threshold=infer_clone_threshold_tmp,
            plot_signal_noise=False,
            print_clone=False,
            rename_leaf_map=rename_leaf_map,
        )

        adata.obs["inferred_clones"] = df_tmp.sort_values("cell_id")[
            "predicted_clone"
        ].to_numpy()

        sel_idx = pd.isna(adata.obs["inferred_clones"])
        old_clone_array = np.array(adata.obs[clone_key].copy()).astype(str)
        old_clone_array[sel_idx] = "nan"

        df_accuracy = metric.lineage_accuracy_from_leaf_order(old_clone_array[order_x])
        obs_clone_N = len(df_tmp["predicted_clone"].unique())
        estimated_total_clone_N = estimate_clone_number(
            adata,
            plot=False,
            fig_dir=fig_dir,
            data_des=f"Thresh: {infer_clone_threshold_tmp:.2f}",
        )

        if len(df_accuracy) > 0:
            used_threshold_list.append(infer_clone_threshold_tmp)
            accuracy_list.append(df_accuracy["accuracy"].mean())
            fraction_list.append(np.sum(~sel_idx) / len(sel_idx))
            obs_clone_N_list.append(obs_clone_N)
            estimated_total_clone_N_list.append(estimated_total_clone_N)

    df_clone_test = pd.DataFrame(
        {
            "threshold": used_threshold_list,
            "accuracy": accuracy_list,
            "retained_cell_fraction": fraction_list,
            "observed_clone_N": obs_clone_N_list,
            "Estimated_total_clone_N": estimated_total_clone_N_list,
        }
    )
    plt.subplots(figsize=(4, 3))
    sns.scatterplot(data=df_clone_test, x="threshold", y="accuracy")
    plt.xlabel("Weight threshold")
    plt.ylabel("Lineage accuracy")
    plt.subplots(figsize=(4, 3))
    sns.scatterplot(data=df_clone_test, x="threshold", y="retained_cell_fraction")
    plt.xlabel("Weight threshold")
    plt.ylabel("Retained cell fraction")

    plt.subplots(figsize=(4, 3))
    plt.plot(
        df_clone_test["threshold"],
        df_clone_test["observed_clone_N"],
        "*",
        label="Obs_N",
    )
    plt.plot(
        df_clone_test["threshold"],
        df_clone_test["Estimated_total_clone_N"],
        "o",
        label="Esti_Total_N",
    )
    plt.xlabel("Threshold")
    plt.ylabel("Clone number")
    plt.legend()


def estimate_clone_number_from_DARLIN_barcodes(
    pd_series, plot=True, clone_key="inferred_clones"
):
    df = (
        pd.DataFrame({clone_key: list(pd_series.astype(str))})
        .reset_index()
        .groupby(clone_key)
        .agg({"index": "count"})
        .rename(columns={"index": "clone_size"})
    )
    clone_size_stat = {}

    for j in range(1, df[~df.index.isin(["nan"])]["clone_size"].max() + 1):
        clone_size_stat[j] = np.sum(df["clone_size"] == j)

    ## a clone of size 2 is counted as a clone of size 1
    # for j in range(2, df[~df.index.isin(["nan"])]["clone_size"].max() + 1):
    #     clone_size_stat[j - 1] = np.sum(df["clone_size"] == j)

    df_freq = pd.DataFrame(
        {"clone_size": clone_size_stat.keys(), "frequency": clone_size_stat.values()}
    )

    tot_clones = df_freq["frequency"].sum()
    singleton_N = df_freq[df_freq["clone_size"] == 1]["frequency"].values[0]
    singleton_ratio = singleton_N / tot_clones
    doublet_N = df_freq[df_freq["clone_size"] == 2]["frequency"].values[0]
    doublet_ratio = doublet_N / tot_clones

    # Good-Turing estimator
    # inferred_clone_N_1 = tot_clones / (1 - singleton_ratio)

    # Chao1 estimator
    inferred_clone_N_2 = tot_clones + singleton_N**2 / (2 * doublet_N)

    if plot:
        sns.scatterplot(data=df_freq, x="clone_size", y="frequency")
        plt.title(
            f"Obs clone={tot_clones}"
            + "\n"
            + f"Estimated clone_N (Chao1)={inferred_clone_N_2:.0f}"
        )
        plt.xlabel("Clone size")
        plt.ylabel("Frequency")
    return inferred_clone_N_2


def estimate_clone_number(adata, clone_key="inferred_clones", nan_as_size_1=False):
    df = (
        pd.DataFrame({clone_key: adata.obs[clone_key].astype(str).to_list()})
        .reset_index()
        .groupby(clone_key)
        .agg({"index": "count"})
        .rename(columns={"index": "clone_size"})
    )
    clone_size_stat = {}

    if nan_as_size_1:
        # if we set the threshold high, then most of cells will be 'nan', thus inflating the estimation
        clone_size_stat[1] = df.loc["nan"]["clone_size"]
        for j in range(2, df[~df.index.isin(["nan"])]["clone_size"].max() + 1):
            clone_size_stat[j] = np.sum(df["clone_size"] == j)
    else:
        # # a clone of size 2 is counted as a clone of size 1
        # for j in range(2, df[~df.index.isin(["nan"])]["clone_size"].max() + 1):
        #     clone_size_stat[j - 1] = np.sum(df["clone_size"] == j)

        # a clone of size 2 is counted as a clone of size 2
        for j in range(1, df[~df.index.isin(["nan"])]["clone_size"].max() + 1):
            clone_size_stat[j] = np.sum(df["clone_size"] == j)

    df_freq = pd.DataFrame(
        {"clone_size": clone_size_stat.keys(), "frequency": clone_size_stat.values()}
    )

    tot_clones = df_freq["frequency"].sum()
    singleton_N = df_freq[df_freq["clone_size"] == 1]["frequency"].values[0]
    singleton_ratio = singleton_N / tot_clones
    if len(df_freq[df_freq["clone_size"] == 2]["frequency"].values) == 0:
        return np.nan
    else:
        doublet_N = df_freq[df_freq["clone_size"] == 2]["frequency"].values[0]
        doublet_ratio = doublet_N / tot_clones

    # Good-Turing estimator
    # inferred_clone_N_1 = tot_clones / (1 - singleton_ratio)

    # Chao1 estimator
    inferred_clone_N_2 = tot_clones + singleton_N**2 / (2 * doublet_N)

    print(f"Predicted total clones by Chao1: {inferred_clone_N_2:.0f}")

    frac_cell_from_singleton_clone = (
        df_freq[df_freq["clone_size"] == 1].frequency.values[0] / adata.shape[0]
    )

    print(
        f"Fraction of cells from singleton clones: {frac_cell_from_singleton_clone:.2f}"
    )

    return df_freq
