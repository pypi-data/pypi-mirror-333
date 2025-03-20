import os
import time

import multiprocess
import numpy as np
import pandas as pd
import scanpy as sc

from . import metadata, scripts
from .settings import *

###########################
# build adata from raw data
###########################


def generate_similarity_heatmap_for_pseudo_cells(
    data_path,
    selected_key,
    annotation,
    similarity_correction=0,
    source="met",
    threads=10,
    selection_list=None,
    reference="mm10",
    min_cells=5,
    exclude_sex=0,
    read_cutoff=3,
    min_coverage=2,
    conda_script="source /home/wangshouwenLab/wangshouwen/miniconda3/etc/profile.d/conda.sh; conda activate CoSpar_test",
):
    df_sample = metadata.load_sample_info(data_path)
    if selection_list is None:
        # selection_list=list(df_sample[selected_key].dropna().unique())
        valid_rows = df_sample[selected_key].notnull()
        value_counts = df_sample[selected_key][valid_rows].value_counts()
        selected_values = value_counts[value_counts > min_cells].index
        selection_list = list(selected_values)

    pool = multiprocess.Pool(threads)

    ## generate methylation profile for each individual pseudo-cell
    def generate_pseudobulk(sample_tmp):
        script_name = scripts.generate_script_bulk_bigwig(
            data_path,
            source=source,
            group_by=selected_key,
            sample_list=[sample_tmp],
            reference=reference,
            scenario="only_bulk",
            min_cells=min_cells,
        )
        command = f"{conda_script}; python {script_name}"
        os.system(command)

    pool.map(generate_pseudobulk, selection_list)

    ## make the corresponding directories
    pseudo_bulk_data = f"{data_path}/met/cpg_level/pseudobulk/{selected_key}"
    data_path_pseudo = f"{data_path}/pseudocell/{selected_key}/downstream_R/all_data"
    os.makedirs(f"{data_path_pseudo}/met/cpg_level", exist_ok=True)
    os.system(f"ln -sf {pseudo_bulk_data}/* {data_path_pseudo}/met/cpg_level")

    scripts.generate_cell_by_region_matrix(
        data_path_pseudo, selection_list, annotation, threads=threads
    )

    df_sample_coarse = (
        df_sample.groupby(selected_key)
        .agg({"nCG": "sum", "met_rate": "mean"})
        .reset_index()
        .rename(columns={selected_key: "sample"})
    )
    df_sample_coarse["HQ"] = True
    df_sample_coarse[selected_key] = df_sample_coarse["sample"]
    # df_sample_coarse['cell_type']=df_sample_coarse[selected_key].apply(lambda x: x.split('_')[0])
    df_sample_coarse.to_csv(
        f"{data_path_pseudo}/sample_sheet.tsv.gz", compression="gzip", sep="\t", index=0
    )

    groupby = selected_key
    selected = "all"
    source = "met"
    out_dir = f"{data_path_pseudo}/out_dir"
    os.makedirs(out_dir, exist_ok=True)
    clone_key = selected_key  #'cell_type'
    script_name = f"{source_script_dir}/DNA/lineage_reconstruction_from_DNA_met.py"
    save_data_des = f"{groupby}_{selected}_{annotation}_readcutoff{read_cutoff}_minCov{min_coverage}_{source}_ExcludeSex{exclude_sex}_PseudoCell"
    command = f"""
             {conda_script}; python {script_name} \
               --root_dir {data_path_pseudo}  --out_dir {out_dir}  --annotation {annotation} --groupby {groupby} --selected {selected}  --read_cutoff {read_cutoff} \
                --min_cov {min_coverage}  --clone_key {clone_key}  --source {source}  --exclude_sex {exclude_sex}  --save_data_des {save_data_des}   --compute_accuracy 0 \
                --similarity_correction {similarity_correction}
            """
    os.system(command)
    adata_path = f"{out_dir}/{save_data_des}.h5ad"
    print("adata path:")
    print(adata_path)
    return sc.read(adata_path)


def generate_similarity_heatmap_for_pseudo_cells_from_more_info(
    data_path,
    selected_key,
    annotation,
    additional_key=None,
    similarity_correction=0,
    source="met",
    threads=10,
    selection_list=None,
    reference="mm10",
    min_cells=5,
    conda_script="source /home/wangshouwenLab/wangshouwen/miniconda3/etc/profile.d/conda.sh; conda activate CoSpar_test",
):

    df_sample = metadata.load_sample_info(data_path)
    selected_key_list = []
    adata_list = []
    for x in df_sample[additional_key].dropna().unique():
        selected_key_list.append(f"{x}_{selected_key}")
        if f"{x}_{selected_key}" not in df_sample.columns:
            mask = df_sample[additional_key] == x
            df_sample.loc[mask, f"{x}_{selected_key}"] = (
                df_sample[mask][additional_key] + "_" + df_sample[mask][selected_key]
            )
    metadata.backup_and_save_sample_info(df_sample, data_path)

    for selected_key in selected_key_list:
        selection_list = list(df_sample[selected_key].dropna().unique())
        adata_tmp = generate_similarity_heatmap_for_pseudo_cells(
            data_path,
            selected_key,
            annotation,
            source=source,
            threads=threads,
            selection_list=selection_list,
            similarity_correction=similarity_correction,
            reference=reference,
            min_cells=min_cells,
            conda_script=conda_script,
        )
        adata_list.append(adata_tmp)
    return adata_list


def generate_single_CpG_adata(
    cpg_level_path,
    valid_sample_list,
    read_cutoff=1,
    merge_strands=False,
    CpG_ref="mm10",
    selected_region_singleCpG=None,
    exclude_sex=0,
    cores=64,
):

    def load_sample_df(sample):
        df_data_tmp = pd.read_csv(f"{cpg_level_path}/{sample}.tsv.gz", sep="\t")
        df_data_tmp.columns = ["chr", "pos", "met_reads", "nonmet_reads", "rate"]
        df_data_tmp["sample"] = sample
        return df_data_tmp

    if cores > len(valid_sample_list):
        cores = len(valid_sample_list)

    from joblib import Parallel, delayed

    df_list = Parallel(n_jobs=cores)(
        delayed(load_sample_df)(i) for i in valid_sample_list
    )

    df_all = pd.concat(df_list, ignore_index=True)

    # Clear the list to remove references
    df_list.clear()

    print(f"filter chr; time {time.time()}")
    # exclude chrM, and also other regions
    df_all["chr"] = df_all["chr"].astype(str)
    chr_dict = {str(x): f"chr{x}" for x in range(1, 30)}
    chr_dict.update({f"chr{x}": f"chr{x}" for x in range(1, 30)})
    chr_dict.update({"X": "chrX", "Y": "chrY", "chrX": "chrX", "chrY": "chrY"})
    df_all["chr"] = df_all["chr"].map(chr_dict)
    df_all = df_all[~pd.isna(df_all["chr"])]

    print(f"Add chr_pos; time {time.time()}")
    chr_pos = [
        f"{x}_{y}" for x, y in zip(df_all["chr"].to_list(), df_all["pos"].to_list())
    ]
    df_all["chr_pos"] = chr_pos

    if selected_region_singleCpG is not None:
        sel_reg_singleCpG = df_all["chr_pos"].isin(selected_region_singleCpG)
        df_all = df_all[sel_reg_singleCpG]

    if merge_strands:
        if CpG_ref not in ["hg38", "hg19", "mm10", "mm9"]:
            raise ValueError(f"CpG_ref {CpG_ref} is not found")
        CpG_ref_dir = f"{CpG_ref_location}/{CpG_ref}.CpGs_new.bed"
        ##############################
        ## Merge CpGs from two strands: BEGIN
        ###############################
        print(f"Merge CpGs from two strands; time {time.time()}")
        df_ref = pd.read_csv(
            CpG_ref_dir,
            sep="\t",
            names=["chr", "pos", "name", "chr_pos", "chr_pos_neg"],
        )
        strand_dict = dict(
            zip(df_ref["chr_pos_neg"].to_list(), df_ref["chr_pos"].to_list())
        )
        sel_idx = df_all["chr_pos"].isin(df_ref["chr_pos"].to_list())
        df_all_pos = df_all[sel_idx]  # CpGs from the positive strand
        df_all_neg = df_all[~sel_idx]  # CpGs from the negative strand
        df_all_neg["chr_pos"] = df_all_neg["chr_pos"].map(strand_dict).to_list()
        nan_frac = np.sum(pd.isna(df_all_neg["chr_pos"])) / len(df_all_neg)
        print(f"Fraction without mapping: {nan_frac}; time {time.time()}")
        if nan_frac > 0.35:
            print("****************ERROR************************")
            print(
                f"{nan_frac} not mapped. Likely due to use the wrong reference genome. Current reference is {CpG_ref}"
            )
            print("****************ERROR************************")
        df_all_neg_clean = df_all_neg[~pd.isna(df_all_neg["chr_pos"])]
        df_all = pd.concat([df_all_pos, df_all_neg_clean])
        del df_all_pos, df_all_neg, df_all_neg_clean, df_ref, strand_dict
        tot_N = len(df_all)
        df_all = (
            df_all.groupby(["chr_pos", "sample"])
            .agg({"met_reads": "sum", "nonmet_reads": "sum"})
            .reset_index()
        )
        drop_frac = 1 - len(df_all) / tot_N
        print(f"Fraction of reads that are dropped: {drop_frac:.2f}")
        if drop_frac > 0.35:
            print("****************ERROR************************")
            print(
                f"{drop_frac} dropped. Likely due to use the wrong reference genome. Current reference is {CpG_ref}"
            )
            print("****************ERROR************************")

        ##############################
        ## Merge CpGs from two strands: END
        ###############################

    print(f"total reads; time {time.time()}")
    df_all["total_reads"] = (
        df_all["met_reads"].to_numpy() + df_all["nonmet_reads"].to_numpy()
    )
    print(f"filtering by reads and rate; time {time.time()}")
    if read_cutoff > 1:
        df_all = df_all[df_all["total_reads"] >= read_cutoff]

    df_all["rate"] = df_all["met_reads"] / df_all["total_reads"]

    cutoff = 0.01
    df_all = df_all[~((df_all["rate"] > cutoff) & (df_all["rate"] < (1 - cutoff)))]
    df_all.loc[df_all["rate"] <= cutoff, "rate"] = 0
    df_all.loc[df_all["rate"] >= (1 - cutoff), "rate"] = 1

    print(f"pivot and sub_adata generation; time {time.time()}")
    adata = sc.AnnData(
        pd.pivot(df_all, index="sample", columns="chr_pos", values="rate")
    )
    del df_all

    if exclude_sex > 0:
        print(f"Exclude sex chromosome; time {time.time()}")
        var_name_array = np.array([x.split("_")[0] for x in adata.var_names])
        full_var_idx = (var_name_array != "chrX") & (var_name_array != "chrY")
        adata = adata[:, full_var_idx]
    elif exclude_sex < 0:
        print(f"Use only sex chromosome; time {time.time()}")
        var_name_array = np.array([x.split("_")[0] for x in adata.var_names])
        full_var_idx = (var_name_array == "chrX") | (var_name_array == "chrY")
        adata = adata[:, full_var_idx]

    return adata


####################
# Methscan related
####################


def generate_adata_from_methscan_matrix(df_data, matrix_dir, read_cutoff=1):
    df_matrix = df_data[(df_data["coverage"] >= read_cutoff)].pivot(
        columns="col", values="mfracs", index="row"
    )
    df_barcode = pd.read_csv(
        f"{matrix_dir}/barcodes.tsv.gz", compression="gzip", header=None
    )
    df_feature = pd.read_csv(
        f"{matrix_dir}/features.tsv.gz", compression="gzip", header=None
    )

    adata = sc.AnnData(df_matrix.to_numpy())
    adata.obs_names = np.array(df_barcode[0].to_list())[
        np.array(df_matrix.index.to_list()) - 1
    ]
    adata.var_names = np.array(df_feature[0].to_list())[
        np.array(df_matrix.columns.to_list()) - 1
    ]
    return adata


def filter_adata(adata, exclude_sex=0, exclude_chrM=True, min_cell_coverage=2):
    var_name_array = np.array([x.split(":")[0] for x in adata.var_names])
    if exclude_chrM:
        full_var_idx = var_name_array != "chrM"
        adata = adata[:, full_var_idx]  # remove Mitochontria

    ## removing sex related features if needed
    if exclude_sex > 0:
        print("Exclude sex chromosome")
        full_var_idx = (var_name_array != "chrX") & (var_name_array != "chrY")
        adata = adata[:, full_var_idx]
    elif exclude_sex < 0:
        print(f"Use only sex chromosome")
        full_var_idx = (var_name_array == "chrX") | (var_name_array == "chrY")
        adata = adata[:, full_var_idx]

    print(f"full adata shape: {adata.shape}")

    ## filter by coverage
    sel_index = (~np.isnan(adata.X)).sum(
        0
    ) >= min_cell_coverage  # min_coverage * adata.shape[0]
    adata = adata[:, sel_index]
    print(
        f"adata shape removing regions covering less than {min_cell_coverage} cells : {adata.shape}"
    )
    return adata


def load_methscan_matrix(matrix_dir):
    df_data = pd.read_csv(
        f"{matrix_dir}/matrix.mtx.gz", compression="gzip", header=None, sep=" "
    )
    df_data.columns = ["row", "col", "residuals", "mfracs", "coverage"]
    return df_data
    return df_data
