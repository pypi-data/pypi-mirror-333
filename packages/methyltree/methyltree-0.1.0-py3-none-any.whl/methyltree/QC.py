import os

import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import sparse as sci_sparse
from tqdm import tqdm

from .metadata import *
from .settings import *

## First section is basic QC, and the second section is further QC like batch effect,
## checking various correlation metrics.


##############################################

## Basic QC, like mapping efficiency, CpG and GpC counts, MT acc rate vs global rate etc.

##############################################


def generate_chr_stats(compact_file_dir, recompute=False):
    if os.path.exists(f"{compact_file_dir}/df_chr_rate.csv") and (not recompute):
        df_chr_rate = pd.read_csv(f"{compact_file_dir}/df_chr_rate.csv", index_col=0)
        df_chr_nCG = pd.read_csv(f"{compact_file_dir}/df_chr_nCG.csv", index_col=0)
    else:
        file_list = [
            x.split(".npz")[0]
            for x in os.listdir(compact_file_dir)
            if x.endswith(".npz")
        ]  # and x.startswith('chr') and (x not in ['chrX.npz','chrY.npz','chrM.npz'])]
        rate_dict = {}
        nCG_dict = {}
        for _ in tqdm(file_list):
            mat = sci_sparse.load_npz(f"{compact_file_dir}/{_}.npz")
            # mat=mat[abs(mat).sum(1).A.flatten()>0]
            diff = mat.sum(0)
            tot_sites = abs(mat).sum(0)
            met_rate = (diff + tot_sites) / (2 * tot_sites)
            rate_dict[_] = list(met_rate.A[0])
            nCG_dict[_] = list(tot_sites.A[0])
        df_chr_rate = pd.DataFrame(rate_dict)
        df_chr_rate.to_csv(f"{compact_file_dir}/df_chr_rate.csv")
        df_chr_nCG = pd.DataFrame(nCG_dict)
        df_chr_nCG.to_csv(f"{compact_file_dir}/df_chr_nCG.csv")
    return df_chr_rate, df_chr_nCG


def extract_mapping_efficiency_core(file_path, mapping_mode="SE"):
    """
    Given the mapping_efficiency summary file, return a dataframe
    """

    ## convert to pandas file
    raw_data = (
        open(file_path).read().split("\n-------------------------------------")[1:]
    )

    sample_names = []
    mapping_efficiency_R1 = []
    mapping_efficiency_R2 = []
    total_C_R1 = []
    total_C_R2 = []

    for line in raw_data:
        temp = line.split("\n-------------")
        sample_names.append(temp[0].split("----------------------------")[0])

        mapping_efficiency_R1.append(
            temp[1].split("\nMapping efficiency:\t")[-1].split("%")[0]
        )
        total_C_R1.append(temp[1].split("Total number of C's analysed:\t")[-1])

        if mapping_mode == "SE":
            mapping_efficiency_R2.append(
                temp[2].split("\nMapping efficiency:\t")[-1].split("%")[0]
            )
            total_C_R2.append(temp[2].split("Total number of C's analysed:\t")[-1])

    if mapping_mode == "SE":
        df_info = pd.DataFrame(
            {
                "Mapping_R1": mapping_efficiency_R1,
                "Mapping_R2": mapping_efficiency_R2,
                "Total_C_R1": total_C_R1,
                "Total_C_R2": total_C_R2,
            }
        )
        df_info = df_info.replace("R2-unmapped--------", "nan")
        df_info = df_info.replace("R1-unmapped--------", "nan")
        df_info = df_info.dropna()
        df_info = df_info.astype(float)
        df_info["Mapping_all"] = df_info["Mapping_R1"] + df_info["Mapping_R2"]
        df_info["Total_C_all"] = df_info["Total_C_R1"] + df_info["Total_C_R2"]

    else:
        df_info = pd.DataFrame(
            {
                "Mapping_all": mapping_efficiency_R1,
                "Total_C_all": total_C_R1,
            }
        )
        df_info = df_info.replace("---PE-------------", "nan")
        df_info = df_info.dropna()
        df_info = df_info.astype(float)

    df_info["sample"] = sample_names
    df_info = df_info.loc[
        :,
        [
            "sample",
            "Mapping_all",
            "Total_C_all",
        ],
    ]

    return df_info


def extract_CpG_CHG_CHH_rate(file_path):
    """
    Given the rate file, return a dataframe
    """

    ## convert to pandas file
    raw_data = (
        open(file_path).read().split("\n-------------------------------------")[1:]
    )

    sample_names = []
    CpG_rate = []
    CHG_rate = []
    CHH_rate = []

    for line in raw_data:
        temp = line.split("-------------")
        sample_names.append(temp[0])

        CpG_rate.append(
            temp[-1].split("\nC methylated in CpG context:\t")[-1].split("%")[0]
        )
        CHG_rate.append(
            temp[-1].split("\nC methylated in CHG context:\t")[-1].split("%")[0]
        )
        CHH_rate.append(
            temp[-1].split("\nC methylated in CHH context:\t")[-1].split("%")[0]
        )

    df_info = pd.DataFrame(
        {
            "CpG_rate": CpG_rate,
            "CHG_rate": CHG_rate,
            "CHH_rate": CHH_rate,
        }
    )

    df_info = df_info.dropna()
    df_info = df_info.astype(float)
    df_info["sample"] = sample_names

    return df_info


def QC_mapping_efficiency(
    root_dir, force_run=False, mapping_mode="SE", genome_reference="mm10"
):
    """
    root_dir: directory leading to the folder of 'met,acc'
    """

    df_sample = load_sample_info(root_dir)
    SampleList = df_sample["sample"].to_numpy()
    file_path = f"{root_dir}/results/all_reports_mapping_efficiency.txt"
    output_file = f"{root_dir}/results/mapping_efficiency.csv"
    if os.path.exists(output_file):
        df_info = pd.read_csv(output_file)
        SampleList = SampleList[~np.in1d(SampleList, df_info["sample"])]
        if len(SampleList) > 0:
            print(f"There are {len(SampleList)} uncomputed samples")
            force_run = True

    if (not os.path.exists(output_file)) or force_run:
        print(f"Recompute!")
        os.system(f"mkdir -p {root_dir}/results")
        command = f"sh {source_script_dir}/DNA/extract_reports.sh {root_dir}/../../bismark  {root_dir}/results {mapping_mode}"
        os.system(command)
        df_info = extract_mapping_efficiency_core(file_path, mapping_mode=mapping_mode)
        df_info.to_csv(output_file, index=0)

    plot_key = "Mapping_all"
    df_info_temp = df_info.sort_values(plot_key).reset_index().dropna()
    ax = sns.scatterplot(x=df_info_temp.index, y=df_info_temp[plot_key], s=10)
    ax.set_xlabel("Sample ordering")
    ax.set_ylabel("Mapping efficiency")
    return df_info


def QC_CpG_CHG_CHH_rate(root_dir, mapping_mode="SE", force_run=False):
    """
    root_dir: directory leading to the folder of 'met,acc'
    """

    df_sample = load_sample_info(root_dir)
    SampleList = df_sample["sample"].to_numpy()
    file_path = f"{root_dir}/results/all_reports_methylation_rate.txt"
    output_file = f"{root_dir}/results/CpG_CHG_CHH_rate.csv"
    if os.path.exists(output_file):
        df_info = pd.read_csv(output_file)
        SampleList = SampleList[~np.in1d(SampleList, df_info["sample"])]
        if len(SampleList) > 0:
            print(f"There are {len(SampleList)} uncomputed samples")
            force_run = True

    if (not os.path.exists(output_file)) or force_run:
        print(f"Recompute!")
        command = f"sh {source_script_dir}/DNA/extract_reports.sh {root_dir}/../../bismark  {root_dir}/results  {mapping_mode}"
        # print(command)
        os.system(f"mkdir -p {root_dir}/results")
        os.system(command)

        df_info = extract_CpG_CHG_CHH_rate(file_path)
        df_info.to_csv(output_file, index=0)

    return df_info


def QC_coverage_report_core(
    root_dir,
    source="met",
    feature_dir=default_feature_dir,
    weight_cutoff=1,
    feature_list=[
        "prom_2000_2000",
        "genebody",
        "prom_2000_2000_cgi",
        "prom_2000_2000_noncgi",
        "CGI",
        "LINE",
        "LTR",
    ],
):
    df_list = []
    for feature in feature_list:
        print(f"---------Current feature: {feature} -----------")

        if source == "met":
            df_data = load_met(root_dir, feature)
        elif source == "acc":
            df_data = load_acc(
                root_dir, feature
            )  # ["sample", "id", "anno", "Nmet", "N", "rate"],
        else:
            raise ValueError

        df_temp = df_data[df_data["N"] >= weight_cutoff]
        df_temp_v2 = (
            df_temp.groupby(["sample", "anno"])
            .agg(
                unique_id_N=("id", "count"),
                average_reads=("N", "mean"),
                average_rate=("rate", "mean"),
            )
            .reset_index()
        )

        bed_info = pd.read_table(f"{feature_dir}/{feature}.bed")
        bed_info.columns = ["chr", "start", "end", "strand", "id", "region"]
        tot_anno_N = len(list(set(bed_info["id"])))
        df_temp_v2["coverage"] = df_temp_v2["unique_id_N"] / tot_anno_N
        df_list.append(df_temp_v2)

    df_merge = pd.concat(df_list, ignore_index=True)
    return df_merge


def QC_coverage_report(
    root_dir,
    source="met",
    feature_dir=default_feature_dir,
    weight_cutoff=1,
    feature_list=[
        "prom_2000_2000",
        "genebody",
        "prom_2000_2000_cgi",
        "prom_2000_2000_noncgi",
        "CGI",
        "LINE",
        "LTR",
    ],
    force_run=False,
):
    """
    root_dir should be where 'acc, met' folder is.
    """

    df_sample = load_sample_info(root_dir)
    SampleList = df_sample["sample"].to_numpy()
    print(f"In total {len(set(SampleList))} samples")

    file_path = (
        f"{root_dir}/results/feature_coverage_{source}_cutoff{weight_cutoff}.csv"
    )
    if os.path.exists(file_path) and (not force_run):
        df_merge = pd.read_csv(file_path)
        # extract the un-computed samples
        SampleList = SampleList[~np.in1d(SampleList, df_merge["sample"].unique())]
        if len(SampleList) > 0:
            print(f"Sample list has been updated! Compute!")
            df_merge = QC_coverage_report_core(
                root_dir,
                feature_dir=feature_dir,
                source=source,
                weight_cutoff=weight_cutoff,
                feature_list=feature_list,
            )

    else:
        df_merge = QC_coverage_report_core(
            root_dir,
            source=source,
            feature_dir=feature_dir,
            weight_cutoff=weight_cutoff,
            feature_list=feature_list,
        )

    df_merge.to_csv(file_path, index=0)
    ax = sns.violinplot(
        data=df_merge[df_merge["anno"].isin(feature_list)], x="anno", y="coverage"
    )
    plt.xticks(rotation=90)
    ax.set_ylabel(f"Coverage (>={weight_cutoff}C)")
    ax.set_xlabel("")
    ax.set_title(source)

    return df_merge


def QC_profile_core(root_dir, SampleList, annotation="prom_2000_2000"):
    """
    Compute methylation and accessibility profiles for a given sample list, and return
    the data in a dataframe.
    """

    # check samples
    un_ready_samples = []
    ready_samples = []

    corr_list = []
    site_N = []
    GC_min = []
    GC_max = []
    CG_min = []
    CG_max = []
    for j in tqdm(range(len(SampleList))):
        sample = SampleList[j]
        data_path = f"{root_dir}/results/metacc/profiles/data/precomputed_metacc_{annotation}_{sample}.txt.gz"
        if not os.path.exists(data_path):
            un_ready_samples.append(sample)
        else:
            df = pd.read_csv(data_path)
            df_out = (
                df.groupby(["cell", "anno", "dist", "context"])
                .agg(mean_rate=("rate", "mean"))
                .reset_index()
            )
            shared_sites = set(df_out[df_out["context"] == "CG"]["dist"]).intersection(
                set(df_out[df_out["context"] == "GC"]["dist"])
            )
            if len(shared_sites) > 5:  # avoid division error from correlation
                df_CG = df_out[df_out["context"] == "CG"]
                df_GC = df_out[df_out["context"] == "GC"]
                shared_site_N = len(shared_sites)
                df_CG_sub = df_CG[df_CG["dist"].isin(shared_sites)]
                df_GC_sub = df_GC[df_GC["dist"].isin(shared_sites)]
                corr_met = np.corrcoef(abs(df_CG_sub["dist"]), df_CG_sub["mean_rate"])[
                    0, 1
                ]
                corr_acc = np.corrcoef(abs(df_GC_sub["dist"]), df_GC_sub["mean_rate"])[
                    0, 1
                ]
                corr_met_acc = np.corrcoef(
                    df_CG_sub["mean_rate"], df_GC_sub["mean_rate"]
                )[0, 1]
                corr_list.append([corr_met, corr_acc, corr_met_acc])
                site_N.append(shared_site_N)
                GC_min.append(df_GC["mean_rate"].min())
                GC_max.append(df_GC["mean_rate"].max())
                CG_min.append(df_CG["mean_rate"].min())
                CG_max.append(df_CG["mean_rate"].max())
                ready_samples.append(sample)

    if len(un_ready_samples) > 0:
        print(f"These samples are not ready: {un_ready_samples}")

    if len(corr_list) > 0:
        corr_list = np.array(corr_list)
        df = pd.DataFrame(
            {
                "sample": ready_samples,
                "corr_met": corr_list[:, 0],
                "corr_acc": corr_list[:, 1],
                "corr_met_acc": corr_list[:, 2],
                "shared_sites": site_N,
                "acc_min": GC_min,
                "acc_max": GC_max,
                "met_min": CG_min,
                "met_max": CG_max,
            }
        )
    else:
        df = pd.DataFrame(
            None,
            columns=[
                "sample",
                "corr_met",
                "corr_acc",
                "corr_met_acc",
                "shared_sites",
                "acc_min",
                "acc_max",
                "met_min",
                "met_max",
            ],
        )

    return df


def QC_profile_core_only_met(root_dir, SampleList, annotation="prom_2000_2000"):
    corr_list = []
    ready_samples = []
    un_ready_samples = []
    CG_min = []
    CG_max = []
    for j in tqdm(range(len(SampleList))):
        sample = SampleList[j]
        profiles_data_path = f"{root_dir}/results/metacc/profiles/data/precomputed_metacc_{annotation}_{sample}.txt.gz"
        if not os.path.exists(profiles_data_path):
            un_ready_samples.append(sample)
        else:
            df_profile = pd.read_csv(profiles_data_path)
            df_out = (
                df_profile.groupby(["cell", "anno", "dist", "context"])
                .agg(mean_rate=("rate", "mean"))
                .reset_index()
            )
            df_CG = df_out[df_out["context"] == "CG"]
            if len(df_CG) > 5:
                corr_met = np.corrcoef(abs(df_CG["dist"]), df_CG["mean_rate"])[0, 1]
            else:
                corr_met = np.nan
            corr_list.append(corr_met)
            CG_min.append(df_CG["mean_rate"].min())
            CG_max.append(df_CG["mean_rate"].max())
            ready_samples.append(sample)

    if len(un_ready_samples) > 0:
        print(f"These samples are not ready: {un_ready_samples}")

    if len(corr_list) > 0:
        corr_list = np.array(corr_list)
        df = pd.DataFrame(
            {
                "sample": ready_samples,
                "corr_met": corr_list,
                "met_min": CG_min,
                "met_max": CG_max,
            }
        )
        df["met_range"] = df["met_max"] - df["met_min"]
    else:
        df = pd.DataFrame(
            None,
            columns=["sample", "corr_met", "met_min", "met_max", "met_range"],
        )
    return df


def QC_profile(root_dir, force_run=False, annotation="prom_2000_2000", only_met=False):
    df_sample = load_sample_info(root_dir)
    SampleList = df_sample["sample"].to_numpy()
    print(f"In total {len(set(SampleList))} samples")

    file_path = f"{root_dir}/results/profile_summary_{annotation}.csv"
    if os.path.exists(file_path) and (not force_run):
        df_0 = pd.read_csv(file_path)
        # extract the un-computed samples
        SampleList = SampleList[~np.in1d(SampleList, df_0["sample"])]
        if len(SampleList) > 0:
            print(f"Compute remaining {len(SampleList)} samples")
            print(SampleList)
            if only_met:
                df_1 = QC_profile_core_only_met(
                    root_dir, SampleList, annotation=annotation
                )
            else:
                df_1 = QC_profile_core(root_dir, SampleList, annotation=annotation)
            df = pd.concat([df_0, df_1], ignore_index=True)
        else:
            df = df_0
    else:
        if only_met:
            df = QC_profile_core_only_met(root_dir, SampleList, annotation=annotation)
        else:
            df = QC_profile_core(root_dir, SampleList, annotation=annotation)

    df.to_csv(file_path, index=0)
    return df


def plot_profile(root_dir, sample, annotation="prom_2000_2000"):
    data_path = f"{root_dir}/results/metacc/profiles/data/precomputed_metacc_{annotation}_{sample}.txt.gz"
    df = pd.read_csv(data_path)
    df_out = (
        df.groupby(["cell", "anno", "dist", "context"])
        .agg(mean_rate=("rate", "mean"))
        .reset_index()
    )
    sns.scatterplot(data=df_out, x="dist", y="mean_rate", hue="context")

    # .merge(df[df['context']=='GC'],on=['cell','id','anno','dist'])


def QC_count_reads(root_dir, force_run=False):
    """
    root_dir should be the directory to 'config.yaml'
    Running this is too slow. So, we will not use this.
    """

    file_path = f"{root_dir}/results/read_counts.csv"
    if os.path.exists(file_path) and (not force_run):
        df = pd.read_csv(file_path)
    else:
        df_sample = load_sample_info(root_dir)
        SampleList = df_sample["sample"].to_numpy()

        output_file = f"{root_dir}/read_counts.txt"
        os.system(f"echo '' > {output_file}")  # create an empty file

        for j in tqdm(range(len(SampleList))):
            sample = SampleList[j]
            file = f"{root_dir}/../raw_fastq/{sample}/{sample}_R1.fastq.gz"
            os.system(
                f"gzip -d -c {file} | wc -l >> {output_file}"
            )  # create an empty file

        # process the data
        df = pd.DataFrame(
            pd.read_csv(f"{root_dir}/read_counts.txt", sep="\t", header=None)[0]
            .apply(lambda x: x.split(" "))
            .to_list()
        ).rename(columns={0: "line_N", 1: "file_name"})
        df["read_N"] = df["line_N"].astype(int) / 4
        df["sample"] = df["file_name"].apply(
            lambda x: x.split("/")[-1].split("_R1.fastq.gz")[0]
        )
        df.to_csv(file_path, index=0)

        return df


def file_size_core(root_dir, SampleList):
    file_size_list = []
    file_name_list = []
    for j in tqdm(range(len(SampleList))):
        sample = SampleList[j]
        file = f"{root_dir}/../../../raw_fastq/{sample}/{sample}_R1.fastq.gz"
        file_size_list.append(os.path.getsize(file))
        file_name_list.append(f"{sample}_R1.fastq.gz")

    file_size_list = np.array(file_size_list)
    # process the data
    df = pd.DataFrame(
        {
            "sample": SampleList,
            "FileName": file_name_list,
            "file_size (byte)": file_size_list,
            "file_size (M)": np.round(file_size_list / 10**6),
            "file_size (G)": np.round(file_size_list / 10**9),
        }
    )
    return df


def QC_file_size(root_dir, force_run=False):
    """
    root_dir should be the directory to 'met,acc' folder
    """

    df_sample = load_sample_info(root_dir)
    SampleList = df_sample["sample"].to_numpy()
    print(f"In total {len(set(SampleList))} samples")

    file_path = f"{root_dir}/results/sample_size.csv"
    if os.path.exists(file_path) and (not force_run):
        df_0 = pd.read_csv(file_path)
        # extract the un-computed samples
        SampleList = SampleList[~np.in1d(SampleList, df_0["sample"])]
        if len(SampleList) > 0:
            print(f"Compute remaining {len(SampleList)} samples")
            df_1 = file_size_core(root_dir, SampleList)
            df = pd.concat([df_0, df_1], ignore_index=True)
        else:
            df = df_0
    else:
        df = file_size_core(root_dir, SampleList)

    df.to_csv(file_path, index=0)
    return df


def extract_count_statistics(root_dir, SampleList, source="met", cores=64):
    """
    Extract the CpG and GpC count number and global met/acc rate,
    as well as rate for MT and lambda DNA for a given SampleList.

    Do not save, but return a dataframe
    """

    def extract_count_statistics_core(sample):
        if source == "met":
            file_name_tmp = f"{root_dir}/met/cpg_level/{sample}.tsv.gz"
        elif source == "acc":
            file_name_tmp = f"{root_dir}/acc/gpc_level/{sample}.tsv.gz"
        else:
            raise ValueError("source should be {met,acc}")

        # print(file_name_tmp)
        df_tmp = pd.read_csv(
            file_name_tmp,
            sep="\t",
            compression="gzip",
            dtype={
                "chr": str,
                "pos": int,
                "met_reads": int,
                "nonmet_reads": int,
                "rate": float,
            },
        )
        unique_C = len(df_tmp)
        Nmet_reads = df_tmp["met_reads"].astype(int).sum()
        Nnonmet_reads = df_tmp["nonmet_reads"].astype(int).sum()
        N_tot_reads = Nmet_reads + Nnonmet_reads
        rates_tmp = df_tmp["rate"].mean()

        unique_chr = list(df_tmp["chr"].unique())
        if "lambda" in unique_chr:
            lambda_label = "lambda"
        elif "lambda_NEB" in unique_chr:
            lambda_label = "lambda_NEB"
        else:
            lambda_label = "J02459"

        if "chrM" in unique_chr:
            MT_label = "chrM"
        elif "MT" in unique_chr:
            MT_label = "MT"
        else:
            MT_label = "M"

        if "L09137" in unique_chr:
            puc19_label = "L09137"
        else:
            puc19_label = "pUC19"

        MT_rate_tmp = df_tmp[df_tmp["chr"] == MT_label]["rate"].mean()
        df_lambda = df_tmp[df_tmp["chr"] == lambda_label]
        lambda_rate_tmp = df_lambda["rate"].mean()
        lambda_CpG_count = len(df_lambda)
        lambda_read_count = (
            df_lambda["met_reads"].sum() + df_lambda["nonmet_reads"].sum()
        )

        df_puc19 = df_tmp[df_tmp["chr"] == puc19_label]
        puc19_rate_tmp = df_puc19["rate"].mean()
        puc19_CpG_count = len(df_puc19)
        puc19_read_count = df_puc19["met_reads"].sum() + df_puc19["nonmet_reads"].sum()
        return [
            source,
            sample,
            unique_C,
            Nmet_reads,
            Nnonmet_reads,
            N_tot_reads,
            rates_tmp,
            MT_rate_tmp,
            lambda_rate_tmp,
            lambda_CpG_count,
            lambda_read_count,
            puc19_rate_tmp,
            puc19_CpG_count,
            puc19_read_count,
        ]

    from joblib import Parallel, delayed

    data_list = Parallel(n_jobs=cores)(
        delayed(extract_count_statistics_core)(i) for i in SampleList
    )

    if source == "met":
        C_name = "nCG"
    else:
        C_name = "nGC"
    df = pd.DataFrame(
        data_list,
        columns=[
            "source",
            "sample",
            C_name,
            f"{source}_Nmet_reads",
            f"{source}_Nnonmet_reads",
            f"{source}_N_tot_reads",
            f"{source}_rate",
            f"{source}_MT_rate",
            f"{source}_lambda_rate",
            f"{source}_lambda_CpG_count",
            f"{source}_lambda_read_count",
            f"{source}_puc19_rate",
            f"{source}_puc19_CpG_count",
            f"{source}_puc19_read_count",
        ],
    )

    return df


def QC_cpg_and_gpc_counts(
    root_dir,
    source="met",
    force_run=False,
    chunk_size=None,
    cores=64,
):
    """
    root_dir should be the directory to 'acc, met' folders
    """

    file_path = f"{root_dir}/results/DNA_read_counts_{source}.csv"
    df_sample = load_sample_info(root_dir)
    SampleList_0 = df_sample["sample"].to_numpy()
    os.makedirs(f"{root_dir}/results", exist_ok=True)
    print(f"In total {len(set(SampleList_0))} samples")
    SampleList = SampleList_0
    if chunk_size is None:
        chunk_size = len(SampleList)

    if not os.path.exists(file_path) or force_run:
        SampleList = SampleList_0[:chunk_size]
        df = extract_count_statistics(root_dir, SampleList, source=source, cores=cores)
        df.to_csv(file_path, index=0)

    while len(SampleList) > 0:
        df_0 = pd.read_csv(file_path)
        # extract the un-computed samples
        SampleList_1 = SampleList_0[~np.in1d(SampleList_0, df_0["sample"])]
        SampleList = SampleList_1[:chunk_size]
        if len(SampleList) > 0:
            print(f"Remaining {len(SampleList_1)} samples")
            df_1 = extract_count_statistics(
                root_dir, SampleList, source=source, cores=cores
            )
            df = pd.concat([df_0, df_1], ignore_index=True)
        else:
            df = df_0
        df.to_csv(file_path, index=0)
    return df


def plot_lambda_MT_QC(df_info):
    df_info = df_info.sort_values("sample").reset_index()
    for selected_Chr in ["lambda", "MT"]:
        f, axs = plt.subplots(
            1, 2, figsize=(10, 4), gridspec_kw=dict(width_ratios=[4, 4])
        )

        if f"acc_{selected_Chr}_rate" in df_info.columns:
            ax = sns.scatterplot(
                x=df_info.index,
                y=df_info[f"acc_{selected_Chr}_rate"],
                label="acc",
                ax=axs[0],
            )
        ax = sns.scatterplot(
            x=df_info.index,
            y=df_info[f"met_{selected_Chr}_rate"],
            label="met",
            ax=axs[0],
        )
        ax.set_xlabel("Sample order by plate ID")
        ax.set_ylabel(f"Rate ({selected_Chr})")

        if "acc_rate" in df_info.columns:
            ax = sns.scatterplot(
                x=df_info.index,
                y=df_info["acc_rate"],
                label="acc",
                ax=axs[1],
            )
        ax = sns.scatterplot(
            x=df_info.index,
            y=df_info["met_rate"],
            label="met",
            ax=axs[1],
        )
        ax.set_xlabel("Sample order by plate ID")
        ax.set_ylabel("Rate (All chromosomes)")
        f.suptitle(f"{selected_Chr} DNA")
        plt.tight_layout()
