import os

import numpy as np
import pandas as pd
import pyranges as pr
from matplotlib import pyplot as plt

from .settings import *


def generate_singleCpG_within_region_annotation(
    selected_region_annotation="500bp", CpG_ref="mm10", recompute_annotation=False
):
    singleCpG_anno_path = (
        f"{default_feature_dir}/{selected_region_annotation}_singleCpG.bed"
    )
    print(f"singleCpG_anno_path: {singleCpG_anno_path}")

    if not os.path.exists(singleCpG_anno_path) or recompute_annotation:
        print(f"generate new {selected_region_annotation}_singleCpG.bed file")

        if CpG_ref not in ["hg38", "hg19", "mm10", "mm9"]:
            raise ValueError(f"CpG_ref {CpG_ref} is not found")
        CpG_ref_dir = f"{CpG_ref_location}/{CpG_ref}.CpGs_new.bed"

        df_ref = pd.read_csv(
            CpG_ref_dir,
            sep="\t",
            names=["Chromosome", "Start", "name", "chr_pos", "chr_pos_neg"],
        )

        df_ref["End"] = df_ref["Start"] + 1

        df_region = pd.read_csv(
            f"{default_feature_dir}/{selected_region_annotation}.bed",
            sep="\t",
            header=None,
        )
        df_region.columns = [
            "Chromosome",
            "Start",
            "End",
            "sign",
            "chr_start_end",
            "length",
        ]

        chr_dict = {str(x): f"chr{x}" for x in range(1, 30)}
        chr_dict.update({f"chr{x}": f"chr{x}" for x in range(1, 30)})
        chr_dict.update({"X": "chrX", "Y": "chrY", "chrX": "chrX", "chrY": "chrY"})

        df_region["Chromosome"] = df_region["Chromosome"].map(chr_dict)
        df_region = df_region[~pd.isna(df_region["Chromosome"])]

        pr_df_ref = pr.PyRanges(df_ref)
        pr_df_region = pr.PyRanges(df_region)
        df_intersect = pr_df_ref.join(pr_df_region).as_df()
        df_intersect = df_intersect.filter(["chr_pos", "chr_pos_neg"]).drop_duplicates()

        all_chr_pos = (
            df_intersect["chr_pos"].tolist() + df_intersect["chr_pos_neg"].tolist()
        )
        df_all_chr_pos = pd.DataFrame(all_chr_pos, columns=["chr_pos"])
        df_all_chr_pos[["Chromosome", "Start"]] = df_all_chr_pos["chr_pos"].str.split(
            "_", expand=True
        )
        del df_all_chr_pos["chr_pos"]
        df_all_chr_pos["Start"] = df_all_chr_pos["Start"].astype(int)
        df_all_chr_pos["End"] = df_all_chr_pos["Start"] + 1

        df_all_chr_pos["sign"] = "*"
        df_all_chr_pos["chr_start_end"] = (
            "singleCpG_"
            + df_all_chr_pos["Chromosome"].astype(str)
            + "_"
            + df_all_chr_pos["Start"].astype(str)
        )
        df_all_chr_pos["label"] = "singleCpG_region_selection"

        df_all_chr_pos.to_csv(singleCpG_anno_path, sep="\t", header=None, index=False)

    df_CpG = pd.read_csv(
        singleCpG_anno_path,
        sep="\t",
        header=None,
    )
    df_CpG.columns = [
        "Chromosome",
        "Start",
        "End",
        "sign",
        "chr_start_end",
        "label",
    ]
    df_CpG = df_CpG[~pd.isna(df_CpG["Chromosome"])]

    selected_CpG = [
        f"{x}_{y}"
        for x, y in zip(df_CpG["Chromosome"].to_list(), df_CpG["Start"].to_list())
    ]

    return selected_CpG


def zscore(df, key="rate"):
    mean = df[key].mean()
    std = df[key].std()
    return (df[key] - mean) / std


def find_signal_region(
    df, n=5, plot=False, win_thresh=1, consecutive_N=3, peak_height=1.5
):
    import pyranges as pr
    from scipy.signal import argrelextrema

    # n = 5,   number of points to be checked before and after
    ## Find local peaks
    df["max"] = df.iloc[
        argrelextrema(df.rate_zscore.values, np.greater_equal, order=n)[0]
    ]["rate_zscore"]

    df.loc[(df["max"] < peak_height), "max"] = np.nan

    if plot:
        # Plot results
        fig, ax = plt.subplots(figsize=(15, 4))
        df_plot = df.iloc[600:700]
        # plt.scatter(df_plot.index, df_plot['min'], c='r')
        plt.plot(df_plot.index, df_plot["rate_zscore"], "-*r")
        plt.scatter(df_plot.index, df_plot["max"], c="g", s=100)
        plt.show()

    ## Find consecutive positive region
    df_diff = (df["rate_zscore"] > win_thresh).astype(int).diff()
    df_start = df[df_diff == 1]
    df_end = df[df_diff == -1]
    win_size = df.iloc[0]["end"] - df.iloc[0]["start"] + 1
    df_start["end"] = df_start["start"].shift(periods=-1).fillna(10**9).astype(int)
    df_end["end"] = df_end["start"]
    pr_start = pr.PyRanges(
        df_start.rename(columns={"chr": "Chromosome", "start": "Start", "end": "End"})
    )
    pr_end = pr.PyRanges(
        df_end.rename(columns={"chr": "Chromosome", "start": "Start", "end": "End"})
    )
    df_bed = (
        pr_start.join(pr_end)
        .as_df()
        .filter(["Chromosome", "Start", "End_b"])
        .rename(columns={"End_b": "End"})
    )
    df_bed["len"] = df_bed["End"] - df_bed["Start"]
    df_bed["id"] = (
        df_bed["Chromosome"].astype(str)
        + "_"
        + df_bed["Start"].astype(str)
        + "_"
        + df_bed["End"].astype(str)
    )
    df_bed = df_bed[df_bed["len"] / win_size >= consecutive_N]

    # interset with high peaks
    df_pr_1 = pr.PyRanges(
        df[df["max"] > peak_height].rename(
            columns={"chr": "Chromosome", "start": "Start", "end": "End"}
        )
    )
    df_pr_2 = pr.PyRanges(df_bed)
    df_out = df_pr_2.join(df_pr_1).as_df()

    df_out = df_out.set_index("id")
    df_out["max_rate"] = df_out.groupby(["id"]).agg(max_rate=("rate_zscore", "max"))

    df_out = (
        df_out.filter(["Chromosome", "Start", "End", "len", "max_rate"])
        .drop_duplicates()
        .reset_index()[["Chromosome", "Start", "End", "len", "max_rate", "id"]]
    )
    return df_out


#########

# peaks

#########


def find_signal_peaks_v0(
    df, n=5, plot=False, win_thresh=0.5, consecutive_N=3, peak_height=1.5
):
    import pyranges as pr
    from scipy.signal import argrelextrema

    # n = 5,   number of points to be checked before and after
    ## Find local peaks
    df["max"] = df.iloc[
        argrelextrema(df.rate_zscore.values, np.greater_equal, order=n)[0]
    ]["rate_zscore"]

    df.loc[(df["max"] < peak_height), "max"] = np.nan

    if plot:
        # Plot results
        fig, ax = plt.subplots(figsize=(15, 4))
        df_plot = df.iloc[600:700]
        # plt.scatter(df_plot.index, df_plot['min'], c='r')
        plt.plot(df_plot["start"], df_plot["rate_zscore"], "-*r")
        plt.scatter(df_plot["start"], df_plot["max"], c="g", s=100)
        plt.show()

    ## Find consecutive positive region
    df_diff = (df["rate_zscore"] > win_thresh).astype(int).diff()
    df_start = df[df_diff == 1]
    df_end = df[df_diff == -1]
    win_size = df.iloc[0]["end"] - df.iloc[0]["start"] + 1
    df_start["end"] = df_start["start"].shift(periods=-1).fillna(10**9).astype(int)
    df_end["end"] = df_end["start"]
    pr_start = pr.PyRanges(
        df_start.rename(columns={"chr": "Chromosome", "start": "Start", "end": "End"})
    )
    pr_end = pr.PyRanges(
        df_end.rename(columns={"chr": "Chromosome", "start": "Start", "end": "End"})
    )
    df_bed = (
        pr_start.join(pr_end)
        .as_df()
        .filter(["Chromosome", "Start", "End_b"])
        .rename(columns={"End_b": "End"})
    )
    df_bed["len"] = df_bed["End"] - df_bed["Start"]
    df_bed["id"] = (
        df_bed["Chromosome"].astype(str)
        + "_"
        + df_bed["Start"].astype(str)
        + "_"
        + df_bed["End"].astype(str)
    )
    df_bed = df_bed[df_bed["len"] / win_size >= consecutive_N]

    # interset with high peaks
    df_pr_1 = pr.PyRanges(
        df[df["max"] > peak_height].rename(
            columns={"chr": "Chromosome", "start": "Start", "end": "End"}
        )
    )
    df_pr_2 = pr.PyRanges(df_bed)
    df_out = df_pr_1.join(df_pr_2).as_df()

    #     df_out=df_out.set_index('id')
    #     df_out['max_rate']=df_out.groupby(['id']).agg(max_rate=('rate_zscore','max'))

    #     df_out=df_out.filter(['Chromosome','Start','End','len','max_rate']
    #              ).drop_duplicates().reset_index()[['Chromosome','Start','End','len','max_rate','id']]
    return df_out


def find_signal_peaks(
    df_data, source="acc", tile_window_size=100, smooth_size=5, zscore_thresh=2.5
):
    """
    We first tile the genome with tile_window_size, and average the rate within the window, then we locally smooth the
    rate using neighboring smoooth_size locus. Then, we z-score transform the smoothed rate, and using the cutoff zscore_thresh to select the signal region. The intermediate results are inserted to the output df_tile

    source: {'acc', 'met'}
    """
    if "Start" not in df_data.columns:
        df_data["Start"] = df_data["pos"].astype(int)
        df_data["End"] = df_data["pos"].astype(int)
    if "Chromosome" not in df_data.columns:
        df_data["Chromosome"] = df_data["chr"]

    # define the available size of each chromosome
    print(f"Generate {tile_window_size}bp genome tiles and perform intersection")
    df_backbone = df_data.groupby("Chromosome").agg(End=("End", "max")).reset_index()
    df_backbone["Start"] = 0
    df_backbone = df_backbone[df_backbone["Chromosome"] != "chrlambda"]

    df_tile = (
        pr.gf.tile_genome(pr.PyRanges(df_backbone), tile_window_size, tile_last=False)
        .join(pr.PyRanges(df_data))
        .as_df()
    )

    # change the type from catogories to str, to avoid expanding the operation
    # to non-existing chromosomes (which are still trakced in df.cat.categories)

    df_list = []
    for chr_tmp in sorted(df_tile["Chromosome"].cat.categories):
        print(chr_tmp)
        df_tmp = df_tile[df_tile["Chromosome"] == chr_tmp]
        if source == "acc":
            df_tmp = (
                df_tmp.groupby(["Start"])
                .agg(tot_met=("met_sites", "sum"), tot_nonmet=("nonmet_sites", "sum"))
                .assign(rate=lambda x: x["tot_met"] / (x["tot_met"] + x["tot_nonmet"]))
                .reset_index()
            )
        else:
            df_tmp = (
                df_tmp.groupby(["Start"])
                .agg(tot_met=("met_sites", "sum"), tot_nonmet=("nonmet_sites", "sum"))
                .assign(
                    rate=lambda x: 1 - x["tot_met"] / (x["tot_met"] + x["tot_nonmet"])
                )
                .reset_index()
            )
        df_tmp["tot_met"] = df_tmp["tot_met"].astype(int)
        df_tmp["tot_N"] = df_tmp["tot_met"] + df_tmp["tot_nonmet"]

        df_tmp["smooth_rate"] = df_tmp.rolling(
            window=smooth_size, center=True, min_periods=1
        ).agg({"rate": "mean"})

        df_tmp["smooth_rate_zscore"] = zscore(df_tmp, key="smooth_rate")
        df_tmp["signal"] = df_tmp["smooth_rate_zscore"]
        df_tmp.loc[df_tmp["smooth_rate_zscore"] < zscore_thresh, "signal"] = 0
        df_tmp["End"] = df_tmp["Start"] + tile_window_size
        df_tmp["Chromosome"] = chr_tmp

        df_list.append(df_tmp)
    df_out = pd.concat(df_list)
    return df_out


def generate_feature_bed_file_from_signal_peaks(
    df_tile,
    save_name=None,
    signal_key="signal",
    merge=True,
    annotation_name="peak",
):
    """
    Take output from find_signal_peaks, and merge neighboring peaks,
    and convert to a feature bed file saved at given name
    """
    if merge:
        df_bed = pr.PyRanges(df_tile).merge().as_df()
    else:
        df_bed = pr.PyRanges(df_tile).as_df()

    df_bed["Strand"] = "*"
    df_bed["id"] = (
        df_bed["Chromosome"].astype(str)
        + "_"
        + df_bed["Start"].astype(str)
        + "_"
        + df_bed["End"].astype(str)
    )
    df_bed["Annotation"] = annotation_name
    df_bed = df_bed.filter(["Chromosome", "Start", "End", "Strand", "id", "Annotation"])

    if save_name != None:
        print(f"file saved at:\n", f"{default_feature_dir}/{save_name}.bed")
        df_bed.to_csv(
            f"{default_feature_dir}/{save_name}.bed", sep="\t", index=0, header=None
        )

    return df_bed


def tile_stats(df_data, tile_window_size=5000):
    """
    Aggregate data within the tile bin of size tile_window_size,
    and check how many peaks and cell types within each bin

    df_data should have columns ['Chromosome','Start','cell_type']
    """
    assert np.isin(["Chromosome", "Start", "End", "cell_type"], df_data.columns).all()

    if "id" not in df_data.columns:
        df_data["id"] = (
            df_data["Chromosome"].astype(str)
            + "_"
            + df_data["Start"].astype(str)
            + "_"
            + df_data["End"].astype(str)
        )

    df_tile_2 = (
        pr.gf.tile_genome(pr.data.chromsizes(), tile_window_size, tile_last=False)
        .join(pr.PyRanges(df_data))
        .as_df()
    )

    df_new_2 = (
        df_tile_2.groupby(["Chromosome", "Start"])
        .agg(
            celltype_N=("cell_type", lambda x: len(set(x))),
            celltypes=("cell_type", lambda x: ",".join(set(x))),
            peak_N=("id", lambda x: len(set(x))),
        )
        .reset_index()
    )
    df_new_2["End"] = df_new_2["Start"] + tile_window_size
    df_new_2 = df_new_2.dropna()
    return df_new_2


def remove_overlapping(df):
    sel_idx = df.iloc[1:]["start"].to_numpy() >= df.iloc[:-1]["end"].to_numpy()
    sel_idx = [True] + list(sel_idx)
    return df[sel_idx]  # .filter(['start','end','value'])
