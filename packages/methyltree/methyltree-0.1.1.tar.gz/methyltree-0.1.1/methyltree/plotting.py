import os

import cospar as cs
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .settings import color_list, color_list_2

###########

# color

###########


def plot_color_bar(fig, cax_list, hex_color_list):
    import matplotlib as mpl

    if type(cax_list) != list:
        cax_list = [cax_list]
        hex_color_list = [hex_color_list]

    for j, cax in enumerate(cax_list):
        cmaplist = [hex_to_rgb(__[1:]) for __ in hex_color_list[j]]

        # create the new map
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            "Custom cmap", cmaplist, len(hex_color_list[j])
        )

        # define the bins and normalize
        bounds = np.linspace(0, len(hex_color_list[j]), len(hex_color_list[j]) + 1)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        # ax2 = fig.add_axes([0.95, 0.15, 0.03, 0.75])
        cb = mpl.colorbar.ColorbarBase(
            cax,
            cmap=cmap,
            norm=norm,
            spacing="proportional",
            ticks=None,
            boundaries=bounds,
            format="%1i",
        )
        cb.set_ticks([])


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i : i + 2], 16)
        rgb.append(decimal)
    rgb.append(256)
    rgb = np.array(rgb) / 256
    return tuple(rgb)


def get_clone_color_dictionary(
    clone_array,
    initial_clone_color_dict=None,
    order_by_size=True,
    color_choice=0,
):
    background_color = "#ffffff"  ##f0f0f0

    if len(set(clone_array)) == len(clone_array):
        print("use pre-set clone order")
        unique_clones = list(clone_array)  # use the pre-set order
    else:
        df = pd.DataFrame({"clone_id": clone_array}).reset_index()
        if order_by_size:
            df_clone = (
                df.groupby("clone_id")
                .agg(cell_count=("index", "count"))
                .sort_values("cell_count", ascending=False)
                .reset_index()
            )

            unique_clones = df_clone["clone_id"].to_list()
        else:
            unique_clones = list(df["clone_id"].unique())

    if (color_choice % 2) == 0:
        color_coding_temp = color_list.copy()
    else:
        color_coding_temp = color_list_2.copy()

    if initial_clone_color_dict is None:
        clone_color_dict = {}
    else:
        clone_color_dict = initial_clone_color_dict
        for clone_tmp, color_tmp in initial_clone_color_dict.items():
            if clone_tmp in unique_clones:
                unique_clones.remove(clone_tmp)
                if color_tmp in color_coding_temp:
                    color_coding_temp.remove(color_tmp)

    if "nan" in unique_clones:
        unique_clones.remove("nan")
    clone_color_dict["nan"] = background_color

    jmax = len(color_coding_temp) - 1
    for j, x in enumerate(unique_clones):
        if j < jmax:
            clone_color_dict[x] = color_coding_temp[j]
        else:
            clone_color_dict[x] = color_coding_temp[jmax]

    return clone_color_dict


##############

# similarity

##############


def plot_similarity_heatmap_with_clone_label(
    input_X,
    label=None,
    label_x=None,
    label_y=None,
    vmax=None,
    vmin=None,
    figsize=(10, 10),
    fontsize=4,
    save_name=None,
    title=None,
    color_bar=False,
    clone_color_dict=None,
    show_label=True,
    cell_index=None,
    legend_labels=None,
    legend_fontsize=10,
    legend_position="upper left",
    show_legend=True,
):
    """
    Since we need to add a color bar, based on the input labels, we cannot change of the order of index within the cs.pl.heatmap function
    """
    cs.settings.set_figure_params(fontsize=fontsize)
    fig, ax = plt.subplots(figsize=figsize)

    if label_x is None:
        label_x = label
    if label_y is None:
        label_y = label

    if show_label:
        if cell_index is not None:
            label_x_tmp = [f"{cell_index[j]}: {x}" for j, x in enumerate(label_x)]
            label_y_tmp = [f"{cell_index[j]}: {x}" for j, x in enumerate(label_y)]
        else:
            label_x_tmp = label_x.copy()
            label_y_tmp = label_y.copy()
    else:
        label_x_tmp = None
        label_y_tmp = None

    cs.pl.heatmap(
        input_X,
        y_ticks=label_y_tmp,
        x_ticks=label_x_tmp,
        order_map_x=False,
        order_map_y=False,
        vmax=vmax,
        vmin=vmin,
        color_bar=color_bar,
        ax=ax,
    )
    if title is not None:
        plt.title(title)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)

    clone_color_dict = get_clone_color_dictionary(
        label_y, initial_clone_color_dict=clone_color_dict
    )
    color_array = [clone_color_dict[__] for __ in label_y]

    plot_color_bar(
        fig, cax, color_array[::-1]
    )  # we flip the order because the cs.pl.heatmap will also flip y axis

    if show_legend:  # Add condition to show legend
        if legend_labels is None:
            legend_labels = list(clone_color_dict.keys())

        color_label = [clone_color_dict[label] for label in legend_labels]
        handles = []
        for label, color in zip(legend_labels, color_label):
            rect = mpatches.Rectangle((0, 0), 1, 1, color=color, label=label)
            handles.append(rect)

        legend = plt.legend(
            handles=handles,
            fontsize=legend_fontsize,
            bbox_to_anchor=(1.1, 1),
            loc=legend_position,
        )
        legend.set_title(None)

    plt.tight_layout()
    if save_name is not None:
        # os.makedirs(save_dir, exist_ok=True)
        plt.savefig(save_name)
        print(f"figure saved at: {save_name}")


def plot_similarity_heatmap_with_multiple_colorbars(
    adata,
    additional_key_list=None,
    heatmap_vmin_percentile=50,
    heatmap_vmax_percentile=99.5,
    figsize=(10, 9.5),
    max_clone_N=20,
    min_clone_size=2,
    fig_dir=None,
    save_name=None,
    data_des=None,
    show_label=False,
    show_x_label=False,
    title=None,
    rotate_cells=False,
    clone_color_dict_orig=None,
    fontsize=6,
    add_cell_index=True,
    show_legend=True,
    legend_fontsize=10,
    maximum_labels_per_column=40,
    legend_position="upper left",
):
    order_x = adata.uns["order_x"]
    ordered_clone_array = adata.uns["ordered_clone_array"]
    ordered_clone_array = exclude_small_clones(
        ordered_clone_array, max_clone_N=max_clone_N, min_clone_size=min_clone_size
    )

    if add_cell_index:
        cell_index = order_x
    else:
        cell_index = None

    if rotate_cells:
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

    input_X = adata.obsm["X_similarity"][order_x][:, order_x]
    label_list = [ordered_clone_array]
    if additional_key_list is not None:
        for tmp_key in additional_key_list:
            label_tmp = adata.obs[tmp_key].astype(str)[order_x]
            label_tmp = exclude_small_clones(
                label_tmp, max_clone_N=max_clone_N, min_clone_size=min_clone_size
            )
            label_list.append(label_tmp)

    heatmap_vmin = np.percentile(input_X.flatten(), heatmap_vmin_percentile)
    heatmap_vmax = np.percentile(np.triu(input_X, k=1), heatmap_vmax_percentile)

    if heatmap_vmin >= heatmap_vmax:
        print("heatmap_vmax<=heatmap_vmin")
        heatmap_vmin = None
        heatmap_vmax = None

    if show_label:
        if cell_index is not None:
            label_y_tmp = [
                f"{cell_index[j]}: {x}" for j, x in enumerate(label_list[-1])
            ]
        else:
            label_y_tmp = label_list[-1].copy()
    else:
        label_y_tmp = None

    if show_x_label:
        x_ticks = label_y_tmp
    else:
        x_ticks = None

    cs.settings.set_figure_params(fontsize=fontsize)
    fig, ax = plt.subplots(figsize=figsize)
    cs.pl.heatmap(
        input_X,
        y_ticks=label_y_tmp,
        x_ticks=x_ticks,
        order_map_x=False,
        order_map_y=False,
        vmax=heatmap_vmax,
        vmin=heatmap_vmin,
        color_bar=False,
        ax=ax,
    )
    if title is not None:
        plt.title(title)

    divider = make_axes_locatable(ax)

    color_array_list = []
    cax_list = []
    handles_list = []
    for j, label in enumerate(label_list):

        if j == 0:
            clone_color_dict = get_clone_color_dictionary(
                label, initial_clone_color_dict=clone_color_dict_orig, color_choice=j
            )
        else:
            if clone_color_dict_orig is not None:
                missing_clones = set(clone_color_dict.keys()) - set(
                    clone_color_dict_orig.keys()
                )
                for missing_clone in missing_clones:
                    clone_color_dict_orig[missing_clone] = clone_color_dict[
                        missing_clone
                    ]
            else:
                clone_color_dict_orig = clone_color_dict

            clone_color_dict = get_clone_color_dictionary(
                label, initial_clone_color_dict=clone_color_dict_orig, color_choice=j
            )

        color_array = [clone_color_dict[__] for __ in label][::-1]
        color_array_list.append(color_array)

        cax = divider.append_axes("right", size="2.5%", pad=0.1)
        cax_list.append(cax)

        if show_legend:  # Add condition to show legend
            legend_labels = list(clone_color_dict.keys())
            if "nan" in legend_labels:
                legend_labels.remove("nan")
            color_label = [clone_color_dict[label] for label in legend_labels]

            handles = []
            for label, color in zip(legend_labels, color_label):
                rect = mpatches.Rectangle((0, 0), 1, 1, color=color, label=label)
                handles.append(rect)
            handles_list.append(handles.copy())

    plot_color_bar(
        fig, cax_list, color_array_list
    )  # we flip the order because the cs.pl.heatmap will also flip y axis

    if show_legend:
        ncol = int(len(legend_labels) / maximum_labels_per_column) + 1
        legend = plt.legend(
            handles=handles_list[-1],
            fontsize=legend_fontsize,
            bbox_to_anchor=[1.1, 1],
            ncol=ncol,
            loc=legend_position,
        )
        legend.set_title(None)

    plt.tight_layout()

    if save_name is not None:
        plt.savefig(save_name)
    elif (fig_dir is not None) and (data_des is not None):
        save_name = f"{fig_dir}/{data_des}_similarity_matrix_multiple_colorbars.pdf"
        plt.savefig(save_name)


def find_vmax(values, q=99):
    return np.percentile(values, q=q)


def plot_all_stats(
    df_all, figure_path, figsize=(3.5, 3.5), color="#fcae91", data_des=""
):
    ylabel_dict = {
        "mean_accuracy": "Lineage accuracy",
        "memory_strength": "Memory score:\n"
        + r"($\overline{intra.}-\overline{inter.}$)/(std. inter.)",
        "log10Pv": "Signif. of clonal memory:\n" + r"$-$log" + r"$_{10}$(P-value)",
    }

    for sel_key in ["mean_accuracy", "memory_strength", "log10Pv"]:
        fig, ax = plt.subplots(figsize=figsize)

        # 示例数据
        x = df_all["stage"]
        y = df_all[sel_key].values

        # 生成x轴的位置
        x_pos = np.arange(len(x))

        # 绘制柱状图
        plt.bar(x_pos, y, width=0.5, color=color)  # ,fill = False)

        # 设置x轴刻度标签
        plt.xticks(x_pos, x)
        plt.xticks(rotation=90)

        # 设置y轴标签
        plt.ylabel(ylabel_dict[sel_key])

        # 在柱状图的顶部标记额外的数字
        if sel_key == "log10Pv":
            clone_numbers = df_all["clone_N"].values  # 要添加的额外数字列表
            for i in range(len(x_pos)):
                plt.text(
                    x_pos[i],
                    y[i] + max(y) * 0.01,
                    clone_numbers[i],
                    ha="center",
                    va="bottom",
                    fontsize=12,
                )
        if sel_key == "mean_accuracy":
            plt.ylim([0, 1])

        # 显示图形
        # plt.show()
        plt.tight_layout()
        plt.savefig(f"{figure_path}/stats_all_{sel_key}_{data_des}.pdf")


def exclude_small_clones(clone_array, max_clone_N=20, min_clone_size=2):
    df = pd.DataFrame({"clone_id": list(clone_array)}).reset_index()
    df_clone = (
        df.groupby("clone_id")
        .agg(cell_count=("index", "count"))
        .sort_values("cell_count", ascending=False)
        .reset_index()
    )
    if len(df_clone) > max_clone_N:
        df_clone = df_clone.iloc[:max_clone_N]
    df_clone = df_clone[df_clone["cell_count"] >= min_clone_size]
    valid_clones = df_clone["clone_id"].unique()
    new_array = []
    for x in clone_array:
        if x not in valid_clones:
            new_array.append("nan")
        else:
            new_array.append(x)
    return new_array


def display_similarity_matrix(out_dir, SAVE_DATA_DES, clone_key=None):
    from IPython.display import Image, display
    from wand.image import Image as WImage

    if clone_key is None:
        file_name = f"{out_dir}/similarity_matrix_{SAVE_DATA_DES}.pdf"
    else:
        file_name = f"{out_dir}/similarity_matrix_{clone_key}_{SAVE_DATA_DES}.pdf"
    if os.path.exists(file_name):
        display(WImage(filename=file_name))
    else:
        print(f"file not found: {file_name}")


################

# embedding

################


def plot_multiple_clones_on_embedding(
    adata,
    clone_key,
    sel_clone_set=None,
    figure_path=".",
    clone_prefix=None,
    title="",
    initial_clone_color_dict=None,
    max_sel_clone=None,
    figsize=(5, 3.5),
    fontsize=13,
    marker_size=100,
    line_width=0.5,
    color_choice=0,
    save_data_des="",
    basis="X_umap",
    background_size=50,
    maximum_labels_per_column=12,
):

    df_clone_0 = (
        pd.DataFrame({clone_key: list(adata.obs[clone_key])})
        .reset_index()
        .groupby(clone_key)
        .agg({"index": "count"})
        .rename(columns={"index": "clone_size"})
    )
    df_clone_1 = (
        df_clone_0[df_clone_0["clone_size"] > 1]
        .sort_values("clone_size", ascending=False)
        .reset_index()
    )

    all_clones = df_clone_1[clone_key].to_numpy().astype(str)

    if "nan" in list(all_clones):
        nan_symbol = "nan"
    else:
        nan_symbol = "NA"

    if sel_clone_set is None:
        if max_sel_clone is None:
            max_sel_clone = len(df_clone_1)
        sel_clone_set = list(all_clones[:max_sel_clone])  #
        if nan_symbol in sel_clone_set:
            sel_clone_set.remove(nan_symbol)

    if clone_prefix is not None:
        new_order = [
            f"{clone_prefix}_{y}"
            for y in sorted(
                [int(x.split(f"{clone_prefix}_")[1]) for x in sel_clone_set]
            )
        ]
    else:
        new_order = sorted(sel_clone_set)

    adata.obs["Clone ID"] = adata.obs[clone_key].map(
        dict(zip(sel_clone_set, sel_clone_set))
    )
    adata.obs["Clone ID"] = adata.obs["Clone ID"].astype(str)  # turn NAN to 'nan'

    clone_color_dict = get_clone_color_dictionary(
        sel_clone_set,
        initial_clone_color_dict=initial_clone_color_dict,
        color_choice=color_choice,
    )

    #########
    ### plot and save the embedding
    #########
    fig, ax = plt.subplots(figsize=figsize)
    cs.settings.set_figure_params(
        pointsize=marker_size, figsize=figsize, fontsize=fontsize
    )
    ax = cs.pl.plot_adata_with_prefered_order(
        adata,
        "Clone ID",
        plot_order=[nan_symbol] + new_order,
        background="nan",
        palette=clone_color_dict,
        s=marker_size,
        linewidth=line_width,
        edgecolor="k",
        background_size=background_size,
        basis=basis,
    )

    # Get the legend handles
    handles, labels = ax.get_legend_handles_labels()
    labels = np.array(labels)
    handles = np.array(handles)
    sel_idx = labels != "nan"

    # # Iterate through the handles and call `set_edgecolor` on each
    # for ha in handles:
    #     ha.set_edgecolor("k")
    #     ha.set_linewidth(0.5)

    # Use `ax.legend` to set the modified handles and labels
    ncol = int(np.sum(sel_idx) / maximum_labels_per_column) + 1
    lgd = ax.legend(
        handles[sel_idx],
        labels[sel_idx],
        loc=[1.05, 0],
        ncol=ncol,
        frameon=False,
    )
    # plt.legend(frameon=False)
    plt.title(title)

    plt.tight_layout()
    plt.savefig(f"{figure_path}/{save_data_des}_all_clone_{clone_key}.pdf")


#########################################

# tree (related, see viewtree package)

#########################################


def plot_tree_with_support(
    tree_path, figsize=(10, 15), leaf_name_map=None, show_support=True
):
    """
    leaf_name_map can be a dictionary or a function to map the old name to new name.

    Try this:
    leaf_name_map=dict(zip(np.arange(adata_final.shape[0]).astype(str), adata_final.obs_names))
    """
    import matplotlib.pyplot as plt
    from Bio import Phylo
    from ete3 import Tree

    with open(f"{tree_path}", "r") as f:
        if show_support:
            my_tree = Tree(f.read(), format=0)
        else:
            my_tree = Tree(f.read(), format=1)
    if leaf_name_map is not None:
        for leaf in my_tree.iter_leaves():
            if type(leaf_name_map) is dict:
                leaf.name = leaf_name_map[leaf.name]  # This is a dictionary
            else:
                leaf.name = leaf_name_map(leaf.name)  # This is a function

    if show_support:
        my_tree = my_tree.write(format=0)
    else:
        my_tree = my_tree.write(format=1)
    with open(f"{tree_path}_tmp.txt", "w") as f:
        f.write(my_tree)

    tree = Phylo.read(f"{tree_path}_tmp.txt", "newick")

    fig, ax = plt.subplots(figsize=figsize)
    plt.ion()
    Phylo.draw(tree, axes=ax)
    ax.axis("off")
    plt.show()


#########################################

# random

#########################################


def boxplot_for_differential_activity(
    df_data, df_sample, genome_id, genome_id_key="id", source="acc", plot_type="boxplot"
):
    df_gene = (
        df_data[df_data[genome_id_key] == genome_id]
        .merge(df_sample.filter(["sample", "celltype", "HQ"]), on="sample")
        .query("HQ==True")
    )  # Spp1, Dppa2,'Tex19.1'
    fig, ax = plt.subplots()
    if plot_type == "boxplot":
        sns.boxplot(data=df_gene, x="celltype", y="rate")
    else:
        sns.violinplot(data=df_gene, x="celltype", y="rate")
    sns.stripplot(data=df_gene, x="celltype", y="rate", size=4, color=".3", linewidth=0)
    plt.xticks(rotation=90)
    plt.xlabel("")
    if source == "acc":
        plt.ylabel("Accessibility rate")
    else:
        plt.ylabel("Methylation rate")
    plt.title(f"{genome_id}; sample N= {len(df_gene)}")


def visualize_raw_rates(
    df_data_list,
    chr_id="2",
    start_N=105130000,
    end_N=105930000,
    color=["r", "b", "k", "g", "yellow", "cyan"],
    pos_key="pos",
    marker=".",
    y_key="rate",
    chr_key="chr",
    merge_track=False,
):
    """
    chr_id: {'1','2','3'...,'X','Y'}

    Note that y_key can be a str, or a list.
    You will need to run the following command to obtain the best effect
    ```jupyter
    %config InlineBackend.figure_format = 'svg' #'retina'         # or 'svg'
    ```
    """
    import seaborn as sns

    sns.set_style("white")
    rcParams["axes.spines.right"] = False
    rcParams["axes.spines.top"] = False
    rcParams["font.size"] = 13
    rcParams["lines.markersize"] = 10

    if (type(y_key) == str) and (type(df_data_list) == list):
        y_key = [y_key for _ in df_data_list]

    if (type(df_data_list) == pd.DataFrame) and (type(y_key) == list):
        df_data_list = [df_data_list for _ in y_key]

    if (type(df_data_list) == pd.DataFrame) and (type(y_key) == str):
        df_data_list = [df_data_list]
        y_key = [y_key]

    if len(color) < len(df_data_list):
        raise ValueError("Please provide more colors if you want more than 4")

    if merge_track:
        fig, ax = plt.subplots(figsize=(30, len(df_data_list)))
    else:
        fig, axs = plt.subplots(
            len(df_data_list), 1, figsize=(30, 3 * len(df_data_list))
        )
    for j, df_test in enumerate(df_data_list):
        df_test[chr_key] = df_test[chr_key].astype(str)
        df_test[pos_key] = df_test[pos_key].astype(int)

        if chr_id not in list(set(df_test[chr_key])):
            raise ValueError("chr_id should be selected from ", set(df_test[chr_key]))

        if start_N > df_test[pos_key].max():
            raise ValueError("start_N should be smaller than ", df_test[chr_key].max())

        if end_N < df_test[pos_key].min():
            raise ValueError("end_N should be larger than ", df_test[chr_key].min())

        tmp = df_test[df_test[chr_key] == chr_id]
        df_test_0 = tmp[(tmp[pos_key] > start_N) & (tmp[pos_key] < end_N)].sort_values(
            pos_key
        )
        if merge_track:
            ax.plot(df_test_0[pos_key], df_test_0[y_key[j]], marker, color=color[j])
        else:
            axs[j].plot(df_test_0[pos_key], df_test_0[y_key[j]], marker, color=color[j])

    plt.tight_layout()
    plt.show()
