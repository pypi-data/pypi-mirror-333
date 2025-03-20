import os
import random
import warnings

import cospar as cs
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
from ete3 import Tree
from matplotlib import pyplot as plt
from skbio import DistanceMatrix

from . import clone, lineage, metadata, metric, plotting, similarity
from .settings import *

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None  # disable the SettingWithCopyWarning


def methylserver_call(
    raw_data_path,
    metadata_path,
    clone_key,
    out_dir,
    data_des="",
    save_data_des="",
    cell_type_key=None,
    heatmap_additional_key_list=None,
    **kwargs,
):
    """
    Used by the methyltree web portal
    """

    df_new2 = pd.read_csv(raw_data_path, compression="gzip", sep="\t").rename(
        columns={"cell_id": "index"}
    )
    df_out = df_new2.pivot(index="index", columns="genomic_region_id", values="value")
    adata = sc.AnnData(df_out)

    df_sample = pd.read_csv(metadata_path, compression="gzip", sep="\t")
    metadata.update_sample_info_on_adata(adata, df_sample)

    if clone_key not in adata.obs.keys():
        raise ValueError(
            f"clone_key={clone_key}, which is not valid. Must be among {adata.obs.keys()}"
        )

    if cell_type_key == "":
        cell_type_key = None
    if cell_type_key is not None:
        if cell_type_key not in adata.obs.keys():
            raise ValueError(
                f"cell_type_key={clone_key}, which is not valid. Must be among {adata.obs.keys()}"
            )
    if heatmap_additional_key_list is not None:
        for _ in heatmap_additional_key_list:
            if _ not in adata.obs.keys():
                raise ValueError(
                    f"heatmap_additional_key_list={heatmap_additional_key_list}, which is not valid. Must be among {adata.obs.keys()}"
                )

    os.makedirs(out_dir, exist_ok=True)

    adata, stat_out = comprehensive_lineage_analysis(
        out_dir,
        data_path=None,
        save_data_des=save_data_des,
        clone_key=clone_key,
        adata_orig=adata,
        perform_accuracy_estimation=True,
        perform_depth_analysis=True,
        perform_memory_analysis=True,
        cell_type_key=cell_type_key,
        heatmap_additional_key_list=heatmap_additional_key_list,
        update_sample_info=False,
        data_des=data_des,
        **kwargs,
    )
    return adata, stat_out


def comprehensive_lineage_analysis(
    out_dir,
    data_path,
    save_data_des,
    clone_key,
    adata_orig=None,
    selected_idx=None,
    update_sample_info=False,
    compute_similarity=False,
    similarity_method="correlation",
    neighbor_info=None,
    cell_type_key=None,
    similarity_correction=True,
    similarity_correction_method="fast",
    similarity_correction_step_size=0.05,
    similarity_normalize=True,
    remove_celltype_signal=False,
    remove_celltype_signal_method="fast",
    remove_celltype_signal_outlier_thresh=1,
    fig_dir=None,
    data_des="",
    fig_out=True,
    heatmap_ordering_method="UPGMA",
    optimize_tree=False,
    optimize_background_cutoff=0.8,
    optimize_show_legend=True,
    clone_color_dict=None,
    heatmap_title=None,
    heatmap_flip_order=False,
    heatmap_show_label=False,
    permute_cell_order=False,
    heatmap_rotate_cells=False,
    heatmap_vmin_percentile=50,
    heatmap_vmax_percentile=99,
    heatmap_maximum_labels_per_column=40,
    heatmap_fontsize=4,
    heatmap_figsize=(10, 9.5),
    heatmap_show_legend=True,
    heatmap_additional_key_list=None,
    heatmap_max_clone_N=22,
    heatmap_min_clone_size=2,
    perform_clone_inference=False,
    clone_inference_threshold=0.5,
    clone_inference_signal_noise_plot=True,
    clone_inference_print=False,
    perform_coarse_graining=False,
    coarse_grain_figsize=(4, 3.5),
    coarse_grain_vmin=None,
    coarse_grain_normalization=True,
    perform_accuracy_estimation=True,
    perform_memory_analysis=False,
    perform_depth_analysis=False,
    accuracy_key="accuracy",
    save_adata=False,
):
    """
    We use this function to perform systematic lineage analysis on DNA methylation data.

    Module:
    1, Data loading
    2, X_similarity regression to remove noise
        * similarity_correction_std=False,
        * similarity_correction_std_per_celltype=False,
        * similarity_correction_threshold=None,
    3, X_similarity z-score to enhance lineage signal
        * remove_celltype_signal=False,
    4, Lineage tree inference or cell state ordering
        * order_method=['NJ','UPGMA','HierarchicalClustering']
    5, Improve lineage tree with stochastic optimization
        * optimize_tree=False,
        * optimize_background_cutoff=0.8,
    6, Identify putative clones with thresholding
        * identify_clones=False,
        * InfClone_threshold=0.5,
        * InfClone_signal_noise=True,
    7, Clean up ordered_clone_array and compute lineage accuracy
    8, Visualize the X_similarity
        * replot_similarity_matrix=False
    9, Memory analysis
    10, Coarse-grain analysis
    11, Accuracy by depth

    ----------------
    If you want to specify colors for each clone, you can provide clone_color_dict
    """

    #################################
    ##        Data loading
    #################################

    if fig_dir is None:
        fig_dir = f"{out_dir}/figure"
        os.makedirs(fig_dir, exist_ok=True)
    sc.set_figure_params()
    sc.settings.figdir = fig_dir

    if adata_orig is None:
        adata = sc.read(f"{out_dir}/{save_data_des}.h5ad")
    else:
        adata = adata_orig.copy()
        print("use provided adata")
    print("adata shape: ", adata.shape)

    ##########################################
    ## check or update metadata
    ##########################################

    # check if df_sample needs to be updated
    used_key_list = [clone_key, cell_type_key]
    if heatmap_additional_key_list is not None:
        used_key_list = used_key_list + heatmap_additional_key_list
    for _ in used_key_list:
        if _ is not None:
            if _ not in adata.obs.keys():
                df_sample = metadata.load_sample_info(data_path)
                if _ not in df_sample.columns:
                    available_keys = set(adata.obs.keys()).union(set(df_sample.columns))
                    raise ValueError(
                        f"The selected key '{_}' it not available. \nPlease select from {available_keys}"
                    )
                else:
                    update_sample_info = True
                    print(
                        f"Warning: '{_}' is not a valid key. Force to update df_sample"
                    )

    if update_sample_info:
        print("update sample")
        df_sample = metadata.load_sample_info(data_path)
        metadata.update_sample_info_on_adata(adata, df_sample)

    if f"X_similarity_{similarity_method}_raw" not in adata.obsm.keys():
        compute_similarity = True
        if adata_orig is None:
            save_adata = True

    adata, order_x = lineage.methyltree_core(
        adata,
        out_dir,
        save_data_des,
        clone_key,
        compute_similarity=compute_similarity,
        similarity_method=similarity_method,
        similarity_correction=similarity_correction,
        similarity_correction_method=similarity_correction_method,
        similarity_correction_step_size=similarity_correction_step_size,
        similarity_normalize=similarity_normalize,
        remove_celltype_signal=remove_celltype_signal,
        remove_celltype_signal_method=remove_celltype_signal_method,
        remove_celltype_signal_outlier_thresh=remove_celltype_signal_outlier_thresh,
        cell_type_key=cell_type_key,
        neighbor_info=neighbor_info,
        heatmap_ordering_method=heatmap_ordering_method,
        optimize_tree=optimize_tree,
        optimize_background_cutoff=optimize_background_cutoff,
        optimize_show_legend=optimize_show_legend,
        permute_cell_order=permute_cell_order,
        selected_idx=selected_idx,
        fig_out=fig_out,
    )

    X_similarity = adata.obsm["X_similarity"]
    with open(f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}.txt", "r") as f:
        my_tree = Tree(f.read())

    ###############################################
    ## Identify putative clones with thresholding
    ###############################################
    adata.obs["state_info_idx"] = np.arange(adata.shape[0]).astype(str)
    df_state_clone = pd.DataFrame(
        {
            "state_info": adata.obs["state_info_idx"],
            "clone_id": adata.obs[clone_key].to_list(),
        }
    ).sort_values("clone_id")
    df_state_clone.to_csv(f"{out_dir}/state_clone_info_{clone_key}_{save_data_des}.csv")

    if perform_clone_inference:
        rename_leaf_map = dict(
            zip(df_state_clone["state_info"].astype(str), df_state_clone["clone_id"])
        )
        df_tmp = clone.identify_putative_clones(
            X_similarity,
            my_tree,
            weight_threshold=clone_inference_threshold,
            plot_signal_noise=clone_inference_signal_noise_plot,
            print_clone=clone_inference_print,
            rename_leaf_map=rename_leaf_map,
        )

        inferred_clone_N = len(df_tmp["predicted_clone"].unique())
        print(f"Inferred clone number: {inferred_clone_N}")

        adata.obs["inferred_clones"] = df_tmp.sort_values("cell_id")[
            "predicted_clone"
        ].to_numpy()

        sel_idx = pd.isna(adata.obs["inferred_clones"])
        old_clone_array = adata.obs[clone_key].copy().to_numpy()
        old_clone_array[sel_idx] = np.nan
        # switch to new clone_key
        clone_key = "filtered_clone"
        adata.obs[clone_key] = old_clone_array

    ############################################################
    ## Clean up ordered_clone_array and compute lineage accuracy
    ############################################################

    if heatmap_flip_order:
        order_x = np.array(order_x)[::-1]

    ordered_clone_array = np.array(adata.obs[clone_key])[order_x].astype(str)
    unique_clone_set = list(set(ordered_clone_array))

    ## rotate the vector so that the first clone will be put at the end
    ## this is because our algorithm often separates cells from the same clone at the beginning and end

    if heatmap_rotate_cells:
        x0 = ordered_clone_array[0]
        count_0 = 0
        unique_clone_set = list(set(ordered_clone_array))
        if "nan" in unique_clone_set:
            unique_clone_set.remove("nan")

        if len(unique_clone_set) > 1:
            while (ordered_clone_array[count_0] == x0) or (
                ordered_clone_array[count_0] == "nan"
            ):
                count_0 += 1
            ordered_clone_array = np.hstack(
                [
                    ordered_clone_array[count_0:],
                    np.array(ordered_clone_array[:count_0])[::-1],
                ]
            )
            order_x = np.hstack([order_x[count_0:], np.array(order_x[:count_0])[::-1]])

    adata.uns["order_x"] = order_x
    adata.uns["ordered_clone_array"] = ordered_clone_array

    accuracy_stat = {}
    if perform_accuracy_estimation:
        if heatmap_min_clone_size > 1:
            ## exluding these signleton clones will artificially inflate the accuracy. [clone_1,clone_0,clone_1] becomes [clone_1,NAN,clone_1]
            for x0 in unique_clone_set:
                if np.sum(ordered_clone_array == x0) == 1:
                    ordered_clone_array[ordered_clone_array == x0] = "nan"

        np.save(
            f"{out_dir}/lineage_order_{clone_key}_{save_data_des}.npy",
            ordered_clone_array,
        )

        # only consider clones with at least two cells before calculating accuracy
        df_accuracy = metric.lineage_accuracy_from_leaf_order(ordered_clone_array)

        # random accuracy
        num_iterations = 10
        random_accuracies = []
        for _ in range(num_iterations):
            random_clone_array = ordered_clone_array.copy()
            random.shuffle(random_clone_array)
            df_random_accuracy = metric.lineage_accuracy_from_leaf_order(
                random_clone_array
            )
            random_accuracies.append(df_random_accuracy)
        df_random_accuracies_concat = pd.concat(random_accuracies)
        df_random_accuracy = (
            df_random_accuracies_concat.groupby(["clone", "clone_size"])
            .mean()
            .reset_index()
        )
        columns_to_prefix = ["continuity", "accuracy", "entropy", "wassertein"]
        df_random_accuracy.rename(
            columns={col: f"random_{col}" for col in columns_to_prefix}, inplace=True
        )

        df_accuracy = df_accuracy.merge(
            df_random_accuracy, on=["clone", "clone_size"]
        ).sort_values(by="clone")
        print(df_accuracy.head(5))

        for sel_key in [
            "continuity",
            "accuracy",
            "entropy",
            "wassertein",
            "random_continuity",
            "random_accuracy",
            "random_entropy",
            "random_wassertein",
        ]:
            weighted_accuracy = np.sum(
                df_accuracy[sel_key]
                * df_accuracy["clone_size"]
                / df_accuracy["clone_size"].sum()
            )
            mean_accuracy = df_accuracy[sel_key].mean()
            accuracy_stat[f"weighted_{sel_key}"] = weighted_accuracy
            accuracy_stat[f"mean_{sel_key}"] = mean_accuracy

            # print(f"weighted {sel_key}:", weighted_accuracy)
            print(f"mean {sel_key}:", mean_accuracy)

        df_accuracy.to_csv(
            f"{out_dir}/accuracy_{clone_key}_{save_data_des}.csv", index=0
        )
        adata.uns["accuracy"] = accuracy_stat

    #################################################################
    ##  visualize the X_similarity
    #################################################################

    plotting.plot_similarity_heatmap_with_multiple_colorbars(
        adata,
        additional_key_list=heatmap_additional_key_list,
        heatmap_vmin_percentile=heatmap_vmin_percentile,
        heatmap_vmax_percentile=heatmap_vmax_percentile,
        figsize=heatmap_figsize,
        fig_dir=fig_dir,
        data_des=data_des,
        show_label=heatmap_show_label,
        title=heatmap_title,
        rotate_cells=heatmap_rotate_cells,
        clone_color_dict_orig=clone_color_dict,
        fontsize=heatmap_fontsize,
        show_legend=heatmap_show_legend,
        maximum_labels_per_column=heatmap_maximum_labels_per_column,
        max_clone_N=heatmap_max_clone_N,
        min_clone_size=heatmap_min_clone_size,
    )

    ###################
    ## Memory analysis
    ###################

    if perform_memory_analysis:
        background, mean_similarity_list, pvalue_all = memory_analysis(
            adata.obsm["X_similarity"][order_x][:, order_x],
            ordered_clone_array,
            fig_dir=fig_dir,
            save_data_des=data_des,
        )

        obs_mean = np.mean(mean_similarity_list)
        rand_mean = np.mean(background)
        rand_std = np.std(background)
        memory_strength = (obs_mean - rand_mean) / rand_std
        clone_N = len(set([x for x in ordered_clone_array if x != "nan"]))
        accuracy_stat["memory_strength"] = memory_strength
        accuracy_stat["pvalue"] = pvalue_all
        accuracy_stat["clone_N"] = clone_N

    ##############################
    ## Coarse-grain analysis
    ##############################

    if perform_coarse_graining:
        adata.uns["data_des"] = [data_des]
        coarse_grain_analysis(
            adata,
            clone_key,
            vmin=coarse_grain_vmin,
            figsize=coarse_grain_figsize,
            method=heatmap_ordering_method,
            title=heatmap_title,
            normalized_X_similarity=coarse_grain_normalization,
        )

    #########################
    # Accuracy by tree depth
    #########################
    if perform_depth_analysis:
        if heatmap_ordering_method in ["NJ", "UPGMA"]:
            ###############################################
            ## Accuracy at different clone threshold
            ###############################################
            cs.settings.set_figure_params()
            df_stats = metric.accuracy_at_different_similarity_threshold(
                adata.obsm["X_similarity"],
                my_tree,
                np.array(adata.obs[clone_key]),
                accuracy_key=accuracy_key,
            )
            df_stats.to_csv(
                f"{out_dir}/accuracy_at_varying_threshold_{clone_key}_{save_data_des}.csv",
                index=0,
            )

            ### Accuracy by tree depth
            df_accuracy_by_depth = metric.compute_accuracy_by_depth(
                my_tree, (adata.obs[clone_key]), accuracy_key=accuracy_key
            )

            df_plot = (
                df_accuracy_by_depth.groupby("Depth")
                .agg(
                    accuracy=(accuracy_key, "mean"),
                    clone=("clone", lambda x: "@".join(x)),
                )
                .reset_index()
            )
            df_plot["clone_N"] = df_plot["clone"].apply(
                lambda x: len(set(x.split("@")))
            )
            # display(df_plot)
            from matplotlib import rcParams

            color_1 = "#d7301f"
            color_2 = "#225ea8"
            cs.settings.set_figure_params()
            rcParams["axes.spines.right"] = True
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.plot(
                df_plot["Depth"],
                df_plot["accuracy"],
                "o-",
                color=color_1,
            )
            ax2 = plt.twinx()
            ax2.plot(df_plot["Depth"], df_plot["clone_N"], "--", color=color_2)
            ax.set_xlabel("Lineage tree depth")
            ax.set_ylim([0, 1.03])
            ax.set_ylabel(f"Reconstruction {accuracy_key}", color=color_1)
            ax2.set_ylabel("Clone number (size>1)", color=color_2)
            plt.tight_layout()
            rcParams["axes.spines.right"] = False
            plt.savefig(f"{fig_dir}/{data_des}_accuracy_by_depth.pdf")

    adata_path = f"{out_dir}/{save_data_des}.h5ad"
    if save_adata:
        print(f"save data at ")
        print(adata_path)
        selected_fatures = ["sample"] + used_key_list
        if update_sample_info:
            df_sample = metadata.load_sample_info(data_path)
            for x in list(set(df_sample.columns).difference(selected_fatures)):
                del adata.obs[x]
        adata.write(adata_path)

    return adata, accuracy_stat


def estimate_transition_rate(seq_1, seq_2):
    """
    transition_rate=[ [0->0, 0->0.5, 0->1],
                      [0.5->0,0.5->0.5,0.5->1],
                      [1->0,1->0.5,1->1] ]
    """

    transition_rate = np.zeros((3, 3))

    joint_non_nan_index = (~np.isnan(seq_1)) & (~np.isnan(seq_2))
    X = seq_1[joint_non_nan_index]
    Y = seq_2[joint_non_nan_index]
    denominator = []

    for i, x in enumerate([0, 0.5, 1]):
        denominator.append(np.sum(X == x))
        for j, y in enumerate([0, 0.5, 1]):
            transition_rate[i, j] = np.sum((X == x) & (Y == y)) / np.sum((X == x))
    print(f"x=0:{denominator[0]};  x=0.5:{denominator[1]}; x=1:{denominator[2]}")
    print(f"mean_rate_x={np.mean(X)};  mean_rate_y={np.mean(Y)}")
    return transition_rate


def coarse_grain_analysis(
    adata,
    clone_key,
    excluded_states=None,
    vmin=None,
    figsize=(4, 3.5),
    method="UPGMA",
    title="",
    semi_triangular=False,
    min_cell_N_per_group=3,
    normalized_X_similarity=True,
):
    cs.settings.set_figure_params(figsize=figsize, format="pdf")
    adata.obs["state_info"] = adata.obs[clone_key]
    df_count = (
        pd.DataFrame({clone_key: adata.obs[clone_key].to_list()})
        .reset_index()
        .groupby(clone_key)
        .agg({"index": "count"})
        .reset_index()
    )
    excluded_states_0 = list(
        df_count[df_count["index"] < min_cell_N_per_group][clone_key]
    )
    if len(excluded_states_0) > 0:
        print(f"Exclude states with <{min_cell_N_per_group} cells: ", excluded_states_0)

    if excluded_states is None:
        excluded_states = excluded_states_0
    else:
        excluded_states = list(set(excluded_states).union(excluded_states_0))
    cs.pp.initialize_adata_object(adata)
    exclude_idx = pd.isna(adata.obs["state_info"]) | np.array(
        adata.obs["state_info"].isin(excluded_states)
    )
    adata_sub = adata[~exclude_idx]
    adata_sub.obsm["X_similarity"] = adata_sub.obsm["X_similarity"][:, ~exclude_idx]

    data_des_0 = adata_sub.uns["data_des"][0]
    adata_sub.uns["data_des"] = [f"{data_des_0}_{clone_key}"]
    if len(set(adata_sub.obs["state_info"])) > 2:
        cs.tl.fate_coupling(
            adata_sub,
            source="X_similarity",
            normalized_X_similarity=normalized_X_similarity,
        )
        cs.pl.fate_coupling(
            adata_sub,
            source="X_similarity",
            vmin=vmin,
            title=title,
            color_bar_label="Methylation similarity score",
            semi_triangular=semi_triangular,
        )

        result_dict = adata_sub.uns[f"fate_coupling_X_similarity"]
        X_coupling = result_dict["X_coupling"]
        fate_names = result_dict["fate_names"]
        dissimilarity = np.max(X_coupling) - X_coupling
        dissimilarity = dissimilarity - np.min(dissimilarity)
        for j in range(X_coupling.shape[0]):
            dissimilarity[j, j] = 0
        dissimilarity = dissimilarity / np.max(dissimilarity)

        dm = DistanceMatrix(
            dissimilarity,
            [f"{x}" for x in list(np.arange(dissimilarity.shape[0]).astype(str))],
        )

        if method == "UPGMA":
            from biotite.sequence.phylo import upgma

            my_tree = Tree(str(upgma(dissimilarity).to_newick()))
        else:
            from skbio.tree import nj

            my_tree = Tree(str(nj(dm)))
            # from . import lineage_tree
            # my_tree = Tree(str(lineage_tree.nj(dm)))

        name_dict = dict(
            zip(np.arange(len(fate_names)).astype(int).astype(str), fate_names)
        )
        for j, leaf in enumerate(my_tree.iter_leaves()):
            leaf.name = name_dict[leaf.name]
        print(my_tree)
        return my_tree

    else:
        raise ValueError("Must have >=3 cluster to generate trees")


def coarse_grained_coupling(
    adata,
    key_1,
    selected_fates_1=None,
    key_2=None,
    selected_fates_2=None,
    selected_times=None,
):
    """
    Generate coarse-grained coupling from two selected keys
    """

    if key_2 == key_1:
        key_2 = key_1

    adata.obs["state_info"] = adata.obs[key_1]
    cs.pp.initialize_adata_object(adata)
    sel_idx = ~(
        pd.isna(adata.obs["state_info"])
        | pd.isna(adata.obs[key_2])
        | (adata.obs["state_info"] == "nan")
        | (adata.obs[key_2] == "nan")
    )
    adata_sub = adata[sel_idx]
    adata_sub.obsm["X_similarity"] = adata_sub.obsm["X_similarity"][:, sel_idx]

    time_info = np.array(adata_sub.obs["time_info"])
    if selected_times is not None:
        if type(selected_times) is not list:
            selected_times = [selected_times]
    sp_idx_0 = cs.hf.selecting_cells_by_time_points(time_info, selected_times)
    state_annote = adata_sub[sp_idx_0].obs["state_info"]
    (
        mega_cluster_list,
        valid_fate_list,
        fate_array_flat,
        sel_index_list,
    ) = cs.hf.analyze_selected_fates(state_annote, selected_fates_1)

    state_annote_2 = adata_sub[sp_idx_0].obs[key_2]
    (
        mega_cluster_list_2,
        valid_fate_list_2,
        fate_array_flat_2,
        sel_index_list_2,
    ) = cs.hf.analyze_selected_fates(state_annote_2, selected_fates_2)

    Smatrix_0 = adata_sub.obsm["X_similarity"]
    Smatrix = Smatrix_0[sp_idx_0][:, sp_idx_0]
    X_coupling = np.zeros((len(mega_cluster_list), len(mega_cluster_list_2)))
    for j, idx_0 in enumerate(sel_index_list):
        for k, idx_1 in enumerate(sel_index_list_2):
            tmp = Smatrix[idx_0][:, idx_1]
            X_coupling[j, k] = np.median(tmp.flatten())

    return X_coupling, mega_cluster_list, mega_cluster_list_2


def memory_analysis(X_similarity_orig, clone_array, fig_dir=".", save_data_des=""):
    """
    clone_array: clone annotation for each of the element in X_similarity_orig matrix
    """

    clone_array = np.array(clone_array).astype(str)

    X_similarity = X_similarity_orig.copy().astype(float)
    temp_array = X_similarity[np.triu_indices_from(X_similarity, k=1)]
    min_value = temp_array.min()
    max_value = temp_array.max()
    X_similarity = (X_similarity - min_value) / (max_value - min_value)

    for i in range(X_similarity.shape[0]):
        X_similarity[i, i] = np.nan

    # scaled_similarity = X_similarity_orig.copy()
    # scaled_similarity[scaled_similarity > 0.99] = np.mean(scaled_similarity)
    # s_max = np.max(scaled_similarity)
    # s_min = np.min(scaled_similarity)
    # scaled_similarity = (scaled_similarity - s_min) / (s_max - s_min)

    clone_key = "clone"
    df_clone_1 = (
        pd.DataFrame({clone_key: clone_array})
        .reset_index()
        .groupby(clone_key)
        .agg({"index": "count"})
    )
    df_clone_1 = (
        df_clone_1[df_clone_1["index"] > 1]
        .sort_values("index", ascending=True)
        .reset_index()
    )

    all_clone_IDs = df_clone_1[clone_key].astype(str).values
    valid_clone_IDs = [x for x in all_clone_IDs if not x.startswith("nan")]

    # to obtain the background, only use the clones that we know, and set the block to be nan (the remaining will be background)
    clone_similarity_score = {}
    for x in valid_clone_IDs:
        sp_idx = np.nonzero(clone_array == x)[0]
        tmp = X_similarity[sp_idx][:, sp_idx].flatten()
        clone_similarity_score[x] = tmp[~np.isnan(tmp)]
        for i in sp_idx:
            for j in sp_idx:
                X_similarity[i, j] = np.nan

    tmp1 = X_similarity.flatten()
    background = tmp1[~np.isnan(tmp1)]

    import scipy.stats as stats

    # here, we only compute the pvalue for valid clones, exluding nan
    pvalue_list = []
    mean_similarity_list = []
    for x in valid_clone_IDs:
        mean_similarity_list.append(np.mean(clone_similarity_score[x]))
        stat_score, pvalue = stats.ranksums(
            clone_similarity_score[x], background, alternative="greater"
        )
        pvalue_list.append(pvalue)

    import statsmodels.sandbox.stats.multicomp

    # P_value = pvalue_list
    # correction assumes that some of these Pvalues are due to randomness. This may not be true.
    P_value = statsmodels.sandbox.stats.multicomp.multipletests(
        list(pvalue_list), alpha=0.05, method="fdr_bh"
    )[1]

    cs.settings.set_figure_params(pointsize=10, fontsize=14)

    plt.subplots(1, 1, figsize=(4, 8))
    x_tick_index = np.linspace(1, len(pvalue_list), len(pvalue_list))
    plt.barh(x_tick_index[::-1], -np.log10(P_value), color="grey")
    plt.yticks(x_tick_index[::-1], np.array(valid_clone_IDs), rotation=0)
    # Set text labels and properties.
    plt.plot(
        np.zeros(len(x_tick_index)) - np.log10(0.05),
        x_tick_index,
        "--",
        color="#a50f15",
    )
    plt.xlabel("-log10 (Pvalue)")
    plt.tight_layout()
    plt.savefig(f"{fig_dir}/{save_data_des}_pvalue_for_individual_clone.pdf")

    ########## all together
    stat_score, pvalue_all = stats.ranksums(
        mean_similarity_list, background, alternative="greater"
    )

    plt.subplots(1, 1, figsize=(5.5, 3.5))
    color_random = "#a6bddb"
    color_data = "#fdbb84"

    all_data = list(mean_similarity_list) + list(background)
    bins = np.linspace(np.min(all_data), np.max(all_data), 50)
    ax = sns.histplot(
        data=background,
        label="Inter-clone",
        bins=bins,
        stat="probability",
        color=color_random,
    )
    ax = sns.histplot(
        data=mean_similarity_list,
        label="Intra-clone",
        bins=bins,
        stat="probability",
        color=color_data,
        alpha=0.5,
    )
    # ax.legend()
    plt.legend(loc=[1.05, 0.4])
    # ax.set_xlabel("Sister-cell distance")
    plt.xlabel("Average similarity score")
    plt.ylabel("Normalized frequency")
    if pvalue_all > 0.0001:
        plt.title(r" $p=$" + f"{pvalue_all:.4f}")
    else:
        # plt.title(f'{source_map[source]}: Pvalue={pvalue:.2E}')
        plt.title(r" $p=$" + f"{pvalue_all:.2E}")
    plt.tight_layout()
    plt.savefig(f"{fig_dir}/{save_data_des}_memory_pvalue.pdf")

    return background, mean_similarity_list, pvalue_all


def embedding_analysis(
    adata,
    clone_key,
    df_sample=None,
    UMAP_parameters=[10, 10, 0.5],
    normalization=True,
    **kwargs,
):
    if df_sample is not None:
        metadata.update_sample_info_on_adata(adata, df_sample)

    adata.obs[clone_key] = adata.obs[clone_key].astype(str)
    df_tmp = pd.DataFrame(adata.obs[clone_key]).dropna()
    clone_names = df_tmp[clone_key].to_numpy()
    cell_id_names = df_tmp.index
    cs.pp.get_X_clone(adata, cell_id_names, clone_names)
    cs.pp.initialize_adata_object(adata)

    X_adjacency = similarity.rescale_similarity_matrix(adata.obsm["X_similarity"])
    if normalization:
        print("spectrum embedding (with normalization)")
        from sklearn.manifold import spectral_embedding

        eig_map = spectral_embedding(
            X_adjacency,
            n_components=50,
        )
        adata.obsm["X_eig"] = eig_map
        if UMAP_parameters[1] >= eig_map.shape[1]:
            UMAP_parameters[1] = eig_map.shape[1]

    else:
        eig, vec = np.linalg.eig(X_adjacency)
        adata.obsm["X_eig"] = np.real(vec[:, 0:50])

    sc.pp.neighbors(
        adata, n_neighbors=UMAP_parameters[0], n_pcs=UMAP_parameters[1], use_rep="X_eig"
    )  # use n_pcs=50 may be better
    sc.tl.umap(adata, min_dist=UMAP_parameters[2])
    adata.obsm["X_emb"] = adata.obsm["X_umap"]

    plotting.plot_multiple_clones_on_embedding(adata, clone_key, **kwargs)
    return adata
