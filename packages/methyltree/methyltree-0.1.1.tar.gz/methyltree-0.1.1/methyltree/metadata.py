import glob
import os

import numpy as np
import pandas as pd
import scipy.sparse as ssp
import yaml

from .settings import *

## sample operations, and loading various annotation and data file, transfer labels etc.

######################

# change or update with df_sample

######################


def update_sample_info_on_adata(adata, df_sample):
    df_sample = df_sample.set_index("sample")
    shared_frac = (
        len(set(df_sample.index).intersection(adata.obs_names)) / adata.shape[0]
    )
    if shared_frac < 0.5:
        print("adata and df_sample have <50 percent shared values")
    for x in df_sample.columns:
        adata.obs[x] = df_sample[x]
    df_sample = df_sample.reset_index()


def backup_and_save_sample_info(df_sample, root_dir):
    # get the current versions for saving
    file_path = f"{root_dir}/sample_sheet.tsv.gz"
    os.system(f"mkdir -p {root_dir}/old_sample_sheet")
    all_paths = sorted(glob.glob(f"{root_dir}/old_sample_sheet/sample_sheet*.tsv.gz"))
    versions = [
        x.split("/")[-1].split("sample_sheet")[1].split(".tsv.gz")[0] for x in all_paths
    ]
    old_version = [x.split("_v")[1] for x in versions if "_v" in x]
    if len(old_version) == 0:
        cur_version = 1
    else:
        cur_version = np.max(np.array(old_version).astype(int)) + 1

    if os.path.exists(file_path):
        # rename the current version
        os.system(
            f"mv {file_path} {root_dir}/old_sample_sheet/sample_sheet_v{cur_version}.tsv.gz"
        )
        # print(f"mv {file_path} {root_dir}/old_sample_sheet/sample_sheet_v{cur_version}.tsv.gz")
    # save a new version
    df_sample.to_csv(file_path, sep="\t", index=False, compression="gzip")


def initialize_sample_info(root_dir):
    """
    We do not save sample info here
    """
    print("Initialize sample info")
    with open(f"{root_dir}/../../config.yaml", "r") as stream:
        file = yaml.safe_load(stream)
        SampleList = file["SampleList"]
    true_list = [True for __ in range(len(SampleList))]
    lineage = ["1" for __ in range(len(SampleList))]
    df_sample = pd.DataFrame(
        {
            "sample": SampleList,
            "cell": SampleList,
            "pass_accQC": true_list,
            "pass_metQC": true_list,
            "id_met": SampleList,
            "id_acc": SampleList,
            "lineage": lineage,
            "stage": lineage,
        }
    )
    return df_sample


def update_samples_from_config(root_dir):
    df_ini_sample_info = initialize_sample_info(root_dir)
    df_sample = load_sample_info(root_dir, force_run=False)
    df_sample_merge = pd.concat(
        [df_sample, df_ini_sample_info], ignore_index=True
    ).drop_duplicates("sample")
    backup_and_save_sample_info(df_sample_merge, root_dir)
    print(
        f"old_samples: {len(df_sample)}; config samples: {len(df_ini_sample_info)}; merged samples: {len(df_sample_merge)}"
    )
    return df_sample_merge


def update_sample_info_with_RNA(root_dir, adata_rna, id_rna_map=None, save=False):
    """
    The root directory should be leading to a DNA folder with 'met, acc'

    id_rna_map: a dictionary to map 'sample' to 'id_rna'
    """

    # df_sample = pd.read_csv(
    #     f"{root_dir}/results/metacc/qc/sample_metadata_after_metacc_qc.txt.gz",
    #     sep="\t",
    #     compression="gzip",
    # )
    df_sample = load_sample_info(root_dir)

    if id_rna_map is None:
        df_sample["plate"] = df_sample["sample"].apply(lambda x: x.split("_DNA_")[0])
        df_sample["plate_barcode"] = df_sample["sample"].apply(
            lambda x: x.split("_DNA_")[1]
        )

        Lime_barcode = mapping_from_plate_barcode_to_Lime_barcode(
            df_sample["plate_barcode"]
        )

        df_sample["Lime_barcode"] = Lime_barcode
        df_sample["id_rna"] = df_sample["plate"] + "_RNA_" + df_sample["Lime_barcode"]
    else:
        df_sample["id_rna"] = df_sample["sample"].map(id_rna_map)

    df_sample["pass_rnaQC"] = df_sample["id_rna"].isin(adata_rna.obs_names)
    df_sample["HQ"] = df_sample["pass_accQC"] & df_sample["pass_metQC"]

    ## Add RNA annotations
    adata_rna_tmp = adata_rna[adata_rna.obs_names.isin(df_sample["id_rna"])]
    df_sample = df_sample.set_index("id_rna")
    df_UMAP = pd.DataFrame(
        {
            "id_rna": adata_rna_tmp.obs_names,
            "UMAP_rna_x": adata_rna_tmp.obsm["X_umap"][:, 0],
            "UMAP_rna_y": adata_rna_tmp.obsm["X_umap"][:, 1],
        }
    ).set_index("id_rna")
    df_sample.loc[adata_rna_tmp.obs_names, "celltype"] = adata_rna_tmp.obs[
        "cell_type"
    ].astype(str)
    df_sample.loc[adata_rna_tmp.obs_names, "leiden"] = adata_rna_tmp.obs[
        "leiden"
    ].astype(str)
    df_sample.loc[adata_rna_tmp.obs_names, "UMAP_rna_x"] = df_UMAP["UMAP_rna_x"]
    df_sample.loc[adata_rna_tmp.obs_names, "UMAP_rna_y"] = df_UMAP["UMAP_rna_y"]

    df_sample.loc[pd.isna(df_sample["celltype"]), "celltype"] = "nan0"
    df_sample.loc[df_sample["celltype"] == "nan", "celltype"] = "nan0"
    df_sample.loc[pd.isna(df_sample["leiden"]), "leiden"] = "nan0"
    df_sample.loc[df_sample["leiden"] == "nan", "leiden"] = "nan0"

    df_sample["lineage"] = df_sample["celltype"]
    df_sample["lineage"] = [
        "_".join(x.split(" ")) for x in df_sample["lineage"]
    ]  # remove any spaces
    df_sample["stage"] = df_sample["lineage"]
    df_sample["cell"] = df_sample["lineage"]

    df_sample = df_sample.reset_index()
    if save:
        print("save the sample_sheet and rna")
        backup_and_save_sample_info(df_sample, root_dir)
        os.makedirs(f"{root_dir}/rna", exist_ok=True)
        adata_rna.write_h5ad(f"{root_dir}/rna/rna_adata.h5ad")
    return df_sample


def get_plate_barcode_to_Lime_barcode_map():
    df_barcode_map = pd.read_csv(
        f"{help_function_dir}/barcode_map.csv"
    ).filter(["LimeCat_BC", "BC_id_num"])
    num_to_BC = dict(zip(df_barcode_map["BC_id_num"], df_barcode_map["LimeCat_BC"]))

    count = 0
    mapping = {}  # map from a plate ID to the Lime barcode.
    for x in range(1, 13):
        for y in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            count = count + 1
            mapping[f"{y}{x}"] = num_to_BC[
                count
            ]  # map from a plate ID like A10 to a barcode ordering number, and then to the Lime barcode.

    return mapping


def mapping_from_Lime_barcode_to_plate_ID(Lime_barcode):
    XX = get_plate_barcode_to_Lime_barcode_map()
    mapping = dict(zip(XX.values(), XX.keys()))
    return [mapping[x] for x in Lime_barcode]


def mapping_from_plate_barcode_to_Lime_barcode(plate_barcode):
    mapping = get_plate_barcode_to_Lime_barcode_map()
    return [mapping[x] for x in plate_barcode]


def get_methscan_sample_index_map(compact_file_dir):
    df_stats = pd.read_csv(f"{compact_file_dir}/cell_stats.csv")
    df_stats.columns = ["sample", "nCG", "n_meth", "met_rate"]
    df_stats["index"] = np.arange(len(df_stats)) + 1
    sample_index_map = dict(zip(df_stats["sample"], df_stats["index"]))
    return sample_index_map


###########

# load data

###########


def load_sample_info(root_dir, force_run=False):
    """
    Load or initialize (force_run=True) sample_info.
    Note that this is the only place where we use the config.yaml file to
    define the SampleList. The rest of functions will only call load_sample_info
    to define SampleList

    Parameters
    ----------
        root_dir:
            Directory at the downstream_R/all_data/. By default, root_dir will point
            to this place throughput this file
    """
    file_path = f"{root_dir}/sample_sheet.tsv.gz"
    if os.path.exists(file_path) and (not force_run):
        df_sample = pd.read_csv(file_path, sep="\t", compression="gzip")
    else:
        df_sample = initialize_sample_info(root_dir)
        backup_and_save_sample_info(df_sample, root_dir)
    return df_sample


def load_barcode_map():
    df_barcode_map = pd.read_csv(
        f"{help_function_dir}/barcode_map.csv", index_col=0
    )
    return df_barcode_map


def load_gene_map():
    gene_map = pd.read_csv(
        f"{default_feature_dir}/../genes/Mmusculus_genes_BioMart.101.txt", sep="\t"
    )
    gene_map.rename(columns={"ens_id": "id"}, inplace=True)
    return gene_map


def get_gene_id_to_name_dict():
    df_map = load_gene_map()
    return dict(zip(df_map["id"], df_map["symbol"]))


def load_annotation(anno):
    data_dir = f"{default_feature_dir}/{anno}.bed"
    return pd.read_csv(
        data_dir,
        sep="\t",
        header=None,
        names=["chr", "start", "end", "strand", "ens_id", "feature"],
    )


def load_met(root_dir, anno):
    df_met = pd.read_csv(
        f"{root_dir}/met/feature_level/{anno}.tsv.gz",
        sep="\t",
        compression="gzip",
        header=None,
    )
    df_met = df_met.rename(
        columns={0: "sample", 1: "id", 2: "anno", 3: "Nmet", 4: "N", 5: "rate"}
    )
    df_met["Nmet"] = df_met["Nmet"].astype(int)
    df_met["N"] = df_met["N"].astype(int)
    df_met["rate"] = df_met["rate"].astype(float)
    if len(df_met.columns) > 6:
        df_met = df_met.rename(columns={6: "rate_before_correction"})
        df_met["rate_before_correction"] = df_met["rate_before_correction"].astype(
            float
        )
    return df_met


def load_acc(root_dir, anno):
    df_acc = pd.read_csv(
        f"{root_dir}/acc/feature_level/{anno}.tsv.gz",
        sep="\t",
        compression="gzip",
        header=None,
    )
    df_acc = df_acc.rename(
        columns={0: "sample", 1: "id", 2: "anno", 3: "Nmet", 4: "N", 5: "rate"}
    )
    df_acc["Nmet"] = df_acc["Nmet"].astype(int)
    df_acc["N"] = df_acc["N"].astype(int)
    df_acc["rate"] = df_acc["rate"].astype(float)
    if len(df_acc.columns) > 6:
        df_acc = df_acc.rename(columns={6: "rate_before_correction"})
        df_acc["rate_before_correction"] = df_acc["rate_before_correction"].astype(
            float
        )

    return df_acc


def load_rna(root_dir):
    import scanpy as sc

    adata = sc.read(f"{root_dir}/rna/rna_adata.h5ad")
    return adata


def merge_metaccrna(root_dir, anno, gene_map=None):
    # load meta data
    sample_info = pd.read_csv(f"{root_dir}/sample_sheet.tsv.gz", sep="\t")

    # load data
    df_met = load_met(root_dir, anno).filter(
        ["sample", "id", "anno", "Nmet", "N", "rate"]
    )
    df_met.rename(
        columns={"Nmet": "met_Nmet", "N": "met_N", "rate": "met_rate"}, inplace=True
    )

    df_acc = load_acc(root_dir, anno).filter(
        ["sample", "id", "anno", "Nmet", "N", "rate"]
    )
    df_acc.rename(
        columns={"Nmet": "acc_Nmet", "N": "acc_N", "rate": "acc_rate"}, inplace=True
    )

    df_metacc = (
        df_acc.merge(df_met.drop("anno", axis=1), on=["sample", "id"])
        .merge(
            sample_info.filter(
                [
                    "celltype",
                    "stage",
                    "sample",
                    "id_rna",
                    "pass_metQC",
                    "pass_rnaQC",
                    "pass_accQC",
                    "HQ",
                ]
            ),
            on="sample",
        )
        .query("HQ==True")
    )
    if gene_map is None:
        df_gene = load_gene_map()
        gene_map = dict(zip(df_gene["id"], df_gene["symbol"]))
        df_metacc["symbol"] = df_metacc["id"].map(gene_map)
    else:
        df_metacc["Unique_ID"] = anno.split("_nb")[0] + "@" + df_metacc["id"]
        df_metacc["symbol"] = df_metacc["Unique_ID"].map(gene_map)

    adata_rna = load_rna(root_dir)
    df_rna = adata_rna.to_df()

    df_rna = (
        df_rna.reset_index()
        .melt(id_vars=["index"], ignore_index=False)
        .rename(columns={"index": "id_rna", "variable": "symbol", "value": "rna_exp"})
    )

    df_metaccrna = df_metacc.merge(df_rna, on=["id_rna", "symbol"])  # , how="outer")
    return df_metaccrna


######################

# Additional annotation functions

######################


def match_index_between_adata(adata_source, adata_target):
    df_source = pd.DataFrame(
        {
            "id_rna": adata_source.obs_names,
            "source_idx": np.arange(adata_source.shape[0]).astype(int),
        }
    )
    df_target = pd.DataFrame(
        {
            "id_rna": list(adata_target.obs_names),
            "target_idx": np.arange(adata_target.shape[0]).astype(int),
        }
    )
    df_merge = df_source.merge(df_target, on="id_rna")

    # extract a common set of cells
    sel_idx = np.array(df_merge["source_idx"]).astype(int)
    adata_source_v1 = adata_source[sel_idx]
    sel_idx = np.array(df_merge["target_idx"]).astype(int)
    adata_target_v1 = adata_target[sel_idx]
    return adata_source_v1, adata_target_v1


def transfer_labels_from_rna_adata_to_DNA_adata(adata_acc, adata_rna, root_dir):
    import scanpy as sc

    if not ssp.issparse(adata_acc.X):
        adata_acc.X = ssp.csr_matrix(adata_acc.X)

    df_acc = pd.DataFrame(
        {
            "sample": adata_acc.obs_names,
            "acc_idx": np.arange(adata_acc.shape[0]).astype(int),
        }
    )
    df_sample = load_sample_info(root_dir)
    df_acc = df_acc.merge(df_sample, on="sample")
    adata_acc_v0 = adata_acc.copy()
    adata_acc_v0.obs_names = np.array(df_acc["id_rna"].astype(str))
    df_RNA = pd.DataFrame(
        {
            "id_rna": list(adata_rna.obs_names),
            "rna_idx": np.arange(adata_rna.shape[0]).astype(int),
        }
    )
    df_acc = df_acc.merge(df_RNA, on="id_rna")

    # extract a common set of cells
    sel_idx = np.array(df_acc["rna_idx"]).astype(int)
    adata_rna_v1 = adata_rna[sel_idx]
    sel_idx = np.array(df_acc["acc_idx"]).astype(int)
    adata_acc_v1 = adata_acc_v0[sel_idx]

    # transfer label, since they now share a common index (rna_id)
    adata_acc_v1.obs["state_info"] = adata_rna_v1.obs["state_info"]
    adata_acc_v1.obs["fate_bias"] = adata_rna_v1.obs["fate_bias"]
    adata_acc_v1.obs["fate_map"] = adata_rna_v1.obs["fate_map"]
    adata_acc_v1.uns["fate_map_colors"] = adata_rna_v1.uns["fate_map_colors"]
    adata_acc_v1.uns["state_info_colors"] = adata_rna_v1.uns["fate_map_colors"]
    adata_acc_v1.obsm["X_umap_rna"] = adata_rna_v1.obsm["X_umap"]

    sc.pl.embedding(adata_acc_v1, color="fate_map", basis="X_umap", s=200)
    return adata_acc_v1


def merge_pseudo_bulk(
    data_path,
    groupby_key="celltype",
    selected_fates=None,
    source="met",
    save_data_des=None,
):
    """
    selected_fates is the names of precomputed bulk files that will be aggregated together. If selected_fates are not provided, using groupby_key to automatically
    determine selected_fates

    save_data_des: the file name to save the data. If not provided, it will be the same as groupby_key
    """

    if source == "met":
        source_dir = "met/cpg_level"
    else:
        source_dir = "acc/gpc_level"

    df_sample = load_sample_info(data_path)

    if selected_fates is None:
        selected_fates = df_sample[groupby_key].dropna().unique()
        print(f"Selected cluster names: {selected_fates}")
    df_1 = pd.read_csv(
        f"{data_path}/{source_dir}/pseudobulk/{groupby_key}/{selected_fates[0]}.tsv.gz",
        sep="\t",
        compression="gzip",
    )

    if save_data_des is None:
        save_data_des = groupby_key
    file_out = f"{data_path}/{source_dir}/pseudobulk/{save_data_des}.tsv.gz"
    print(f"The results will be saved at {file_out}")

    for x in selected_fates[1:]:
        print(f"Current sample: {x}")
        df_2 = pd.read_csv(
            f"{data_path}/{source_dir}/pseudobulk/{groupby_key}/{x}.tsv.gz",
            sep="\t",
            compression="gzip",
        )
        df_merge = df_1.merge(df_2, on=["chr", "pos"], how="outer").fillna(0)
        df_merge["met_sites"] = df_merge["met_sites_x"] + df_merge["met_sites_y"]
        df_merge["nonmet_sites"] = (
            df_merge["nonmet_sites_x"] + df_merge["nonmet_sites_y"]
        )

        df_merge["met_sites"] = df_merge["met_sites"].astype(int)
        df_merge["nonmet_sites"] = df_merge["nonmet_sites"].astype(int)

        df_merge["rate"] = (
            100
            * df_merge["met_sites"]
            / (df_merge["met_sites"] + df_merge["nonmet_sites"])
        )

        df_merge = df_merge.dropna()

        df_merge["rate"] = (df_merge["rate"]).astype(int)
        df_1 = df_merge.filter(["chr", "pos", "met_sites", "nonmet_sites", "rate"])

    print("save data")
    df_1.to_csv(
        file_out,
        sep="\t",
        compression="gzip",
        index=0,
    )
