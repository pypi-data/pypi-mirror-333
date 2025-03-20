import os

import cospar as cs
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
import skbio
from ete3 import Tree
from matplotlib import pyplot as plt
from matplotlib import rcParams
from skbio import DistanceMatrix

from . import metric, plotting, similarity
from .settings import *


def methyltree_core(
    adata,
    out_dir,
    save_data_des,
    clone_key,
    compute_similarity=False,
    similarity_method="correlation",
    similarity_correction=True,
    similarity_correction_method="fast",
    similarity_correction_step_size=0.05,
    similarity_normalize=True,
    remove_celltype_signal=False,
    remove_celltype_signal_method="fast",
    remove_celltype_signal_outlier_thresh=1,
    cell_type_key=None,
    neighbor_info=None,
    heatmap_ordering_method="UPGMA",
    optimize_tree=False,
    optimize_background_cutoff=0.8,
    optimize_show_legend=True,
    permute_cell_order=False,
    selected_idx=None,
    fig_out=True,
):
    """
    THis core algorithm accept an adata, and performs the following:
    1, compute the similarity matrix
    2, similarity correction
    3, similarity zscore
    4, Build the lineage with NJ method
    """

    os.makedirs(out_dir, exist_ok=True)
    if (
        (cell_type_key is None)
        and (neighbor_info is None)
        and (remove_celltype_signal == True)
    ):
        raise ValueError(
            "Missing cell_type_key or neighbor_info for removing celltype signal"
        )

    clone_id_list = np.array(adata.obs[clone_key]).astype(str)
    clone_id_list = clone_id_list[(clone_id_list != "nan") & (clone_id_list != "NA")]
    if len(set(clone_id_list)) == len(clone_id_list):
        raise ValueError(
            f"clone_key {clone_key} does not have clones with >1 cells. Change clone_key please!"
        )

    ##########################################
    ## check or update similarity matrix
    ##########################################

    raw_similarity_key = f"X_similarity_{similarity_method}_raw"

    if raw_similarity_key not in adata.obsm.keys():
        compute_similarity = True
        print(f"{raw_similarity_key} not found in adata.obsm")
    else:
        X_shape = adata.obsm[raw_similarity_key].shape
        if X_shape[0] != X_shape[1]:
            print(f"Similarity shape mismatch ({X_shape})")
            compute_similarity = True

    if compute_similarity:
        print("re-compute similarity matrix")
        X_similarity, shared_site_matrix = similarity.compute_similarity_matrix(
            adata.X,
            method=similarity_method,
        )
        adata.obsm[raw_similarity_key] = X_similarity
        adata.obsm["X_shared_sites"] = shared_site_matrix
    adata.obsm["X_similarity"] = adata.obsm[raw_similarity_key].copy()

    # permute the adata so that our predicted ordering will not be influenced by the original ordering of the cell
    if permute_cell_order and (neighbor_info is None):
        print("permute ordering")
        permut_idx = np.random.default_rng(seed=42).permutation(adata.shape[0])
        adata = adata[permut_idx]
        adata.obsm["X_similarity"] = adata.obsm["X_similarity"][:, permut_idx]
        if "X_join_N" in adata.obsm.keys():
            adata.obsm["X_join_N"] = adata.obsm["X_join_N"][:, permut_idx]

    ###################################################
    ##   X_similarity regression to remove noise
    ###################################################

    if similarity_correction:
        # the initial rescaling helps to avoid negative correlations
        if similarity_normalize:
            X_similarity_old = similarity.rescale_similarity_matrix(
                adata.obsm["X_similarity"].copy()
            )
        else:
            X_similarity_old = adata.obsm["X_similarity"].copy()
        for _ in range(1):
            currect_epsilon = np.max([similarity_correction_step_size - 0.01 * _, 0.01])
            print(
                f"correct similarity: outer loop {_};  current epsilon {currect_epsilon}"
            )
            X_similarity_new = similarity.correct_similarity_matrix(
                X_similarity_old,
                fig_out=fig_out,
                epsilon=currect_epsilon,
                method=similarity_correction_method,
            )
            tmp = X_similarity_new - X_similarity_old
            tmp_std = np.std((tmp).flatten())
            print(f"std: {tmp_std:.3f}")
            X_similarity_old = X_similarity_new
            if tmp_std < 0.005:
                break

        adata.obsm["X_similarity"] = X_similarity_new

    ###################################################
    ##   X_similarity z-score to enhance lineage signal
    ###################################################
    # generate cell_type_key
    if cell_type_key is not None:
        # get rid of na or NAN, which has no cell type annotation
        adata.obs[cell_type_key] = adata.obs[cell_type_key].astype(str)
        sel_idx = ~adata.obs[cell_type_key].isin(["nan", "NA"])
        if (
            (np.sum(~sel_idx) > 0)
            and (neighbor_info is None)
            and remove_celltype_signal
        ):
            print("Warning: exclude cells with no type annotation")
            adata = adata[sel_idx]
            sel_idx = np.array(sel_idx)
            adata.obsm["X_similarity"] = adata.obsm["X_similarity"][:, sel_idx]
            print(f"New adata shape: {adata.shape}")
        cell_type_array = np.array(adata.obs[cell_type_key]).astype(str)
    else:
        cell_type_array = None

    if remove_celltype_signal:
        if (remove_celltype_signal_method == "fast") and (neighbor_info is None):
            # This method is much faster
            print("Remove cell-type signal with fast method")
            zscore_X_similarity = similarity.remove_celltype_signal_discrete_state(
                adata.obsm["X_similarity"],
                cell_type_array=cell_type_array,
                outlier_threshold=remove_celltype_signal_outlier_thresh,
            )
        else:
            if neighbor_info is None:
                neighbor_info = []
                for j, x in enumerate(cell_type_array):
                    neighbor_IDs = np.nonzero(cell_type_array == x)[0]
                    if len(neighbor_IDs) == 0:
                        neighbor_IDs = np.arange(
                            len(cell_type_array)
                        )  # if NaN, use the entire array as the background
                    neighbor_info.append(neighbor_IDs)

            # This method is very slow
            print("Remove cell-type signal with slow/original method")
            zscore_X_similarity = similarity.remove_celltype_signal_continuous_state(
                adata.obsm["X_similarity"],
                neighbor_info=neighbor_info,
                outlier_threshold=remove_celltype_signal_outlier_thresh,
            )

        adata.obsm["X_similarity"] = zscore_X_similarity

    #############################################################
    ##   show similarity histogram going for downstream analysis
    #############################################################

    if similarity_normalize:
        print("similarity normalize----")
        X_similarity = similarity.rescale_similarity_matrix(
            adata.obsm["X_similarity"].copy()
        )
    else:
        X_similarity = adata.obsm["X_similarity"].copy()

    if selected_idx is not None:
        X_similarity = X_similarity[selected_idx][:, selected_idx]
        adata = adata[selected_idx]

    adata.obsm["X_similarity"] = X_similarity

    if fig_out:
        fig, ax = plt.subplots(figsize=(4, 3))
        tmp_data = (
            np.array(X_similarity[np.triu_indices_from(X_similarity, k=1)]) + 0.01
        )  # 0.01 is pseudocount to avoid zero when taking log in the following histplot
        sns.histplot(tmp_data)
        plt.yscale("log")
        plt.xlabel("Similarity")
        plt.show()

    ###################################################
    ## Lineage tree inference or cell state ordering
    ###################################################
    Allowed_methods = ["NJ", "HierarchicalClustering", "UPGMA", "FASTME"]

    ### Tree reconstruction
    print(f"Reconstruction method: {heatmap_ordering_method}")
    tree_path = f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}.txt"
    if heatmap_ordering_method in ["NJ", "UPGMA", "FASTME"]:
        dissimilarity = np.max(X_similarity) - X_similarity
        dissimilarity = dissimilarity - np.min(dissimilarity)
        for j in range(X_similarity.shape[0]):
            dissimilarity[j, j] = 0
        dissimilarity = dissimilarity / np.max(dissimilarity)
        dm = DistanceMatrix(
            dissimilarity,
            [f"{x}" for x in list(np.arange(dissimilarity.shape[0]).astype(str))],
        )

        if heatmap_ordering_method == "NJ":
            my_tree = skbio.tree.nj(dm)
            # my_tree = lineage_tree.nj(dm, method=NJ_parameter)
            my_tree.write(tree_path)
        elif heatmap_ordering_method == "FASTME":
            f_out = run_fastme(dissimilarity, out_dir)
            my_tree = skbio.TreeNode.read(f_out)
            my_tree.write(tree_path)
        elif heatmap_ordering_method == "UPGMA":
            from biotite.sequence.phylo import upgma

            my_tree = upgma(dissimilarity).to_newick()
            with open(tree_path, "w") as f:
                f.write(my_tree)

        with open(tree_path, "r") as f:
            my_tree = Tree(f.read())

        ######################################################
        ## Improve lineage tree with stochastic optimization
        ######################################################
        if optimize_tree:
            print("Optimize lineage tree")
            my_tree = optimize_lineage_tree(
                adata,
                my_tree,
                background_cutoff=optimize_background_cutoff,
                clone_key=clone_key,
                plot_heatmap=False,
                show_legend=optimize_show_legend,
            )

        order_x = np.array(my_tree.get_leaf_names()).astype(int)

    elif heatmap_ordering_method == "HierarchicalClustering":
        from scipy.cluster.hierarchy import leaves_list, linkage, optimal_leaf_ordering
        from scipy.spatial.distance import pdist, squareform

        # Assume cov_matrix is your covariance matrix
        # Convert covariance to dissimilarity
        dissimilarity = np.max(X_similarity) - X_similarity
        # Convert to condensed distance matrix
        dist_mat = squareform(dissimilarity)
        # Compute linkage matrix
        Z = linkage(dist_mat, method="average")
        # Get the optimal leaf ordering
        order_x = leaves_list(optimal_leaf_ordering(Z, dist_mat))
    else:
        raise ValueError(f"method must be among: {Allowed_methods}")
    return adata, order_x


def bootstrap_lineage_tree(
    adata_orig,
    out_dir,
    save_data_des,
    clone_key,
    cell_type_key=None,
    selected_idx=None,
    num_iterations=100,
    sampled_replacement=False,
    sample_fraction=0.8,
    similarity_correction=False,
    similarity_normalize=True,
    remove_celltype_signal=False,
    fig_dir=None,
    exact_match=False,
    recompute=False,
    heatmap_ordering_method="UPGMA",
    cores=64,
):
    """
    Generate tree support
    """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if fig_dir is None:
        fig_dir = f"{out_dir}/figure"
    sc.set_figure_params()
    sc.settings.figdir = fig_dir

    num_cols_feature = adata_orig.shape[1]
    tree_dict = {}  ## a dictionary for appearance counts of all observed sub-trees
    node_support = {}  ## a dictionary for support values of all observed sub-trees

    parameter_str = f"{heatmap_ordering_method}_frac{sample_fraction}_normalize{similarity_normalize}_correction{similarity_correction}_celltypesignal{remove_celltype_signal}_celltypekey{cell_type_key}"

    ###################################################
    ############## tree from bootstrap
    ###################################################
    def compute_sub_sampled_adata(round_num):
        output_tree_dir = f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}_bootstrap_{round_num}_{parameter_str}.txt"
        if (not os.path.exists(output_tree_dir)) or recompute:
            print(f"num_iterations : {round_num}")
            sample_size = int(sample_fraction * num_cols_feature)

            if sampled_replacement:
                sampled_cols = np.random.choice(
                    num_cols_feature, size=sample_size, replace=True
                )
            else:
                sampled_cols = np.random.choice(
                    num_cols_feature, size=sample_size, replace=False
                )

            adata_bootstrap = adata_orig[:, sorted(sampled_cols)].copy()

            print("adata shape: ", adata_bootstrap.shape)

            # the output of the next step is stored here
            adata_bootstrap, _ = methyltree_core(
                adata_bootstrap,
                out_dir,
                f"{save_data_des}_bootstrap_{round_num}_{parameter_str}",
                clone_key,
                selected_idx=selected_idx,
                fig_out=False,  # to avoid figure printing
                compute_similarity=True,  # force computation of the similarity
                cell_type_key=cell_type_key,
                similarity_correction=similarity_correction,
                similarity_normalize=similarity_normalize,
                remove_celltype_signal=remove_celltype_signal,
            )

    if cores > num_iterations:
        cores = num_iterations

    from joblib import Parallel, delayed

    results = Parallel(n_jobs=cores)(
        delayed(compute_sub_sampled_adata)(i) for i in range(num_iterations)
    )

    for round_num in range(num_iterations):
        output_tree_dir = f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}_bootstrap_{round_num}_{parameter_str}.txt"

        ###################################################
        ### update sub-tree frequency based on current tree
        ###################################################

        ## read bootstrapped tree and compute the frequency of each sub-tree
        with open(output_tree_dir, "r") as f:
            tree_str = f.read().strip()
        tree = Tree(newick=tree_str, format=1)
        # tree.sort_descendants()  ## the original label 0,1,2,..., is abitrary. We should not sort the leaves by this order.
        ## Also, using our fuzzy match method, the result is no longer sensitive to the order of leaf are not longer

        ##  set the tree branch length to be 1 to avoid problems in exact match
        for node in tree.traverse():
            node.dist = 1

        ## update sub-tree freqeuncy
        for node in tree.traverse("postorder"):
            if not node.is_leaf():
                if exact_match:
                    ## when the same set of cells appear in this sub-tree, and the order is also the same
                    subtree_str = node.write()
                else:
                    ## when the same set of cells appear in this sub-tree, but the order can be different
                    subtree_str = ",".join(
                        np.array(
                            sorted(np.array(node.get_leaf_names()).astype(int))
                        ).astype(str)
                    )

                if subtree_str not in tree_dict:
                    tree_dict[subtree_str] = 1
                else:
                    tree_dict[subtree_str] += 1

    ## compute the support value for each sub-tree
    for node in tree_dict:
        node_support[node] = tree_dict[node] / num_iterations

    ###################################################
    ############## original-tree generation
    ###################################################

    orig_tree_dir = (
        f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}_{parameter_str}.txt"
    )
    if (not os.path.exists(orig_tree_dir)) or recompute:
        adata_orig, _ = methyltree_core(
            adata_orig,
            out_dir,
            f"{save_data_des}_{parameter_str}",
            clone_key,
            selected_idx=selected_idx,
            fig_out=False,  # to avoid figure printing
            cell_type_key=cell_type_key,
            similarity_correction=similarity_correction,
            remove_celltype_signal=remove_celltype_signal,
            heatmap_ordering_method=heatmap_ordering_method,
            similarity_normalize=similarity_normalize,
        )

    ############################################
    ### get dictory for updating leaf names
    ############################################

    if selected_idx is not None:
        adata_new = adata_orig[selected_idx].copy()
    else:
        adata_new = adata_orig

    df_state_clone = pd.DataFrame(
        {
            "state_info": np.arange(adata_new.shape[0]).astype(str),
            "clone_id": adata_new.obs[clone_key].to_list(),
        }
    ).fillna("nan")

    df_state_clone.index = df_state_clone["state_info"].to_list()
    clone_name_map = dict(
        zip(df_state_clone["state_info"].astype(str), df_state_clone["clone_id"])
    )
    if cell_type_key is not None:
        df_type = pd.DataFrame(
            {cell_type_key: adata_new.obs[cell_type_key].to_list()}
        ).reset_index()
        cell_type_map = dict(zip(df_type.index.astype(str), df_type[cell_type_key]))

    ##########################################
    ### update support values and save results
    ##########################################

    with open(orig_tree_dir, "r") as f:
        tree_str_tmp = f.read().strip()
    tmp_tree_support = Tree(newick=tree_str_tmp, format=1)
    # tmp_tree_support.sort_descendants()
    ## set the branch length to be uniform, for better visualization
    for node in tmp_tree_support.traverse():
        node.dist = 1

    for node in tmp_tree_support.traverse("postorder"):
        if not node.is_leaf():
            if exact_match:
                subtree_str = node.write()
            else:
                subtree_str = ",".join(
                    np.array(
                        sorted(np.array(node.get_leaf_names()).astype(int))
                    ).astype(str)
                )

            # set the name to be the support value
            if subtree_str in node_support:
                node.name = f"{node_support[subtree_str]:.2f}"
            else:
                node.name = 0

    for j, leaf in enumerate(tmp_tree_support.iter_leaves()):
        if (cell_type_key is None) or (cell_type_key == clone_key):
            new_name = f"{leaf.name}" + "-" + str(clone_name_map[leaf.name])
        else:
            new_name = (
                f"{leaf.name}"
                + "-"
                + str(cell_type_map[leaf.name])
                + "-"
                + clone_name_map[leaf.name]
            )
        leaf.name = new_name

    tmp_tree_support.write(
        format=1,
        outfile=f"{out_dir}/lineage_tree_{clone_key}_{save_data_des}_{heatmap_ordering_method}_support.txt",
    )

    return tmp_tree_support


def run_fastme(dissimilarity, out_dir):

    # Write the distance matrix to a temporary file
    input_file = os.path.join(out_dir, "fastme_tmp.dist")
    precision = 100000
    dissimilarity = (dissimilarity * precision).astype(int) / precision

    name_list = [f"{x}" for x in list(np.arange(dissimilarity.shape[0]).astype(str))]

    with open(input_file, "w") as file:
        file.write(f"{len(name_list)}\n")
        from tqdm import tqdm

        for j, x in tqdm(enumerate(list(dissimilarity))):
            data = "\t".join(x.astype(str))
            file.write(str(name_list[j]) + "\t" + "".join(data) + "\n")

    # Define the output file path
    f_out = os.path.join(out_dir, "fastme_tmp.nwk")

    # Construct the command
    command = f"fastme -i {input_file} -o {f_out} -n -s"

    # Run the command
    exit_code = os.system(command)

    if exit_code != 0:
        raise RuntimeError(f"FastME did not run successfully. Exit code: {exit_code}")

    return f_out


#############################################
## lineage tree operation and optimization
#############################################


def optimize_lineage_tree(
    adata,
    my_tree,
    background_cutoff,
    clone_key,
    iterations=10000,
    plot_heatmap=True,
    plot_history=True,
    show_legend=True,
):
    X_similarity = similarity.rescale_similarity_matrix(
        adata.obsm["X_similarity"].copy()
    )
    order_x = np.array(my_tree.get_leaf_names()).astype(int)

    ## determine clone size scale
    for i in range(X_similarity.shape[0]):
        X_similarity[i, i] = 0
    high_idx = np.nonzero(X_similarity[order_x][:, order_x] > background_cutoff)

    temp = abs(high_idx[0] - high_idx[1])
    clone_size_scale = np.median(temp)
    print(f"Clone size scale: {clone_size_scale}")

    ## define the weight matrix
    for i in range(X_similarity.shape[0]):
        X_similarity[i, i] = 1

    factor = 2
    size = X_similarity.shape[0]
    weight_matrix = np.zeros((size, size))
    for i in range(weight_matrix.shape[0]):
        for j in range(weight_matrix.shape[0]):
            if abs(i - j) > factor * clone_size_scale:
                weight_matrix[i, j] = (
                    np.exp(-factor) * (factor * clone_size_scale) / abs(i - j)
                )  # np.exp(-factor)*(weight_matrix.shape[0]-abs(i-j)+factor*clone_size_scale)/
            else:
                weight_matrix[i, j] = np.exp(-abs(i - j) / clone_size_scale)
            # weight_matrix[i,j]=np.exp(-abs(i-j)/clone_size_scale)

    ## perform optimization
    current_score = np.sum(X_similarity[order_x][:, order_x] * weight_matrix)
    result = []
    from tqdm import tqdm

    for j in tqdm(range(iterations)):
        # my_tree_new=omic_ana.random_subtree_pruning_and_regrafting(my_tree)

        my_tree_new = random_subtree_swapping(my_tree)

        order_x_new = np.array(my_tree_new.get_leaf_names()).astype(int)
        next_score = np.sum(X_similarity[order_x_new][:, order_x_new] * weight_matrix)
        # print(next_score-current_score)

        if next_score > current_score:
            my_tree = my_tree_new
            current_score = next_score

            ordered_clone_array = adata.obs[clone_key].astype(str)[order_x_new]
            unique_clone_set = list(set(ordered_clone_array))
            for x0 in unique_clone_set:
                if np.sum(ordered_clone_array == x0) == 1:
                    ordered_clone_array[ordered_clone_array == x0] = "nan"

            df_accuracy = metric.lineage_accuracy_from_leaf_order(ordered_clone_array)
            mean_accuracy = df_accuracy[df_accuracy["clone_size"] > 1].mean()
            mean_accuracy = mean_accuracy[
                ["accuracy", "entropy", "continuity", "wassertein"]
            ]
            print(f"iter-{j}; score {current_score}; continuity {mean_accuracy[2]}")

            result.append(
                [
                    current_score,
                    mean_accuracy[0],
                    mean_accuracy[1],
                    mean_accuracy[2],
                    mean_accuracy[3],
                ]
            )

    ## plot the results
    if plot_history:
        plt.clf()
        cs.settings.set_figure_params()
        df_tmp = pd.DataFrame(result)
        fig, ax = plt.subplots()
        ax.scatter(df_tmp[0], df_tmp[1], label="accuracy")
        ax.scatter(df_tmp[0], df_tmp[2], label="entropy")
        ax.scatter(df_tmp[0], df_tmp[3], label="continuity")
        ax.scatter(df_tmp[0], df_tmp[4], label="wassertein")
        plt.xlabel("Optimization score")
        plt.ylabel("Accuracy")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    if plot_heatmap:
        vmin = np.percentile(X_similarity.flatten(), 50)
        vmax = np.max(np.triu(X_similarity, k=1))

        plotting.plot_similarity_heatmap_with_clone_label(
            X_similarity[order_x_new][:, order_x_new],
            label=adata.obs[clone_key].astype(str)[order_x_new],
            vmin=vmin,
            vmax=vmax,
            color_bar=False,
            save_name=f"heatmap.pdf",
            # title=title,  # f"{stage}_{annotation}",
            # clone_color_dict=clone_color_dict,
            # show_label=show_label,
            cell_index=None,
            show_legend=show_legend,
        )

    return my_tree


def is_subtree(subtree, tree):
    return subtree.write(format=5)[:-1] in tree.write(format=5)[:-1]


def swap_branches(tree, branch_1, branch_2):
    X = branch_1.write(format=5)[:-1]
    Y = branch_2.write(format=5)[:-1]
    Orig = tree.write(format=5)
    seq_list = Orig.split(X)
    if Y in seq_list[0]:
        final = Y.join([X.join(seq_list[0].split(Y)), seq_list[1]])
    else:
        final = Y.join([seq_list[0], X.join(seq_list[1].split(Y))])
    return Tree(final)


def swap_descendants(tree, descendant1, descendant2):
    # does not add the sub branch_1 to the exactly the same location of branch_2
    up_1 = descendant1.up
    up_2 = descendant2.up
    down_1 = descendant1.detach()
    down_2 = descendant2.detach()
    up_1.add_child(down_2)
    up_2.add_child(down_1)
    return tree


# Define a function to perform random subtree pruning and regrafting
def random_subtree_pruning_and_regrafting(tree_orig):
    tree = tree_orig.copy()
    import random

    # Select a random node for subtree pruning
    branch_1 = random.choice(tree.get_descendants())

    # Select a random target node for regrafting
    # Ensure the target node is not a descendant of the pruned subtree
    while True:
        branch_2 = random.choice(tree.get_descendants())
        if not (is_subtree(branch_2, branch_1) or is_subtree(branch_1, branch_2)):
            break

    # print(branch_1)
    # print(branch_2)

    # return swap_branches(tree, branch_1, branch_2)
    return swap_descendants(tree, branch_1, branch_2)


def random_subtree_swapping(tree_orig):
    tree = tree_orig.copy()
    import random

    # Select a random node for subtree pruning
    branch_1 = random.choice(tree.get_descendants())
    branch_1.swap_children()
    return tree


def traverse_tree_to_update_dist(
    node,
    matrix,
    method="percentile",
    percentile=50,
    rename_leaf_map=lambda x: x.split("-")[0],
):
    leaf_names = node.get_leaf_names()
    if rename_leaf_map is not None:
        sel_idx = np.array([rename_leaf_map(x) for x in leaf_names]).astype(int)
    else:
        sel_idx = np.array(leaf_names).astype(int)

    if len(sel_idx) > 1:
        data = pd.DataFrame(matrix[sel_idx][:, sel_idx].flatten()).dropna()[0].values
        if method == "percentile":
            node.dist = np.percentile(data, percentile)
        elif method == "min":
            node.dist = np.min(data)
        elif method == "mean":
            node.dist = np.mean(data)
        elif method == "median":
            node.dist = np.median(data)
        elif method == "max":
            node.dist = np.max(data)
        else:
            raise ValueError(
                "method should be among {percentile, mean, median, min, max}"
            )
    else:
        node.dist = np.nan
    for child in node.children:
        traverse_tree_to_update_dist(
            child, matrix, method=method, percentile=percentile
        )
