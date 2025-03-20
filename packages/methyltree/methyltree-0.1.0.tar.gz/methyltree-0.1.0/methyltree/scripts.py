import glob
import os

import multiprocess
import pandas as pd
from tqdm import tqdm

from . import metadata
from .settings import *


def generate_cell_by_region_matrix(
    data_path, selected_sample_list, annotation, threads=64
):

    pool = multiprocess.Pool(threads)

    ## annotate each individual pseudo-cell
    def annotate_single_sample(sample_tmp):
        command = f"Rscript {source_script_dir}/Rscripts/annotate/scNMT_annotate_individual_sample.R  --context CG  --basedir {data_path}  --featuresdir {default_feature_dir}  --sample {sample_tmp}  --annos {annotation}"
        os.system(command)

    pool.map(annotate_single_sample, selected_sample_list)

    ## Merge all annotations
    command = f"Rscript {source_script_dir}/Rscripts/annotate/scNMT_annotate_merge.R  --context CG  --basedir {data_path}  --featuresdir {default_feature_dir}   --annos {annotation}"
    os.system(command)
    print("-----JOB Finished-----")


def generate_TSS_profile(data_path, selected_sample_list, annotation, threads=64):

    data_output = f"{data_path}/results/metacc/profiles/data"
    sample_path = f"{data_path}/sample_sheet.tsv.gz"
    df_sample = metadata.initialize_sample_info(data_path)
    df_sample.to_csv(sample_path, sep="\t", index=False, compression="gzip")

    os.makedirs(data_output, exist_ok=True)

    def profile_function_tmp(sample):
        command = f"cd {source_script_dir}/Rscripts; Rscript profiles/calculate_only_met_profiles_SW.R --met_tile 100 --window_size 2000 --metadata {sample_path} \
        --anno {annotation} --out_dir {data_output} --featuredir {default_feature_dir}  --basedir {data_path} --sample {sample} "
        os.system(command)

    pool = multiprocess.Pool(threads)
    pool.map(profile_function_tmp, selected_sample_list)
    print("-----JOB Finished-----")


def generate_script_bulk_bigwig(
    root_path,
    source="acc",
    min_cells=5,
    group_by="lineage",
    sample_list=None,
    metadata_path_0=None,
    reference="mm10",
    step_size=None,
    scenario="all",
):
    print(f"script scenario: {scenario}")
    if scenario not in ["all", "only_bulk", "only_bigwig"]:
        raise ValueError("scenario must be in [all,only_bulk,only_bigwig]")

    os.makedirs(f"{root_path}/scripts", exist_ok=True)
    os.makedirs(f"{root_path}/acc/gpc_level/pseudobulk/{group_by}", exist_ok=True)
    os.makedirs(f"{root_path}/met/cpg_level/pseudobulk/{group_by}", exist_ok=True)

    if metadata_path_0 is None:
        metadata_path_0 = f"{root_path}/sample_sheet.tsv.gz"

    df_all_samples = pd.read_csv(metadata_path_0, sep="\t", compression="gzip")
    df_all_samples = df_all_samples[df_all_samples["HQ"]]
    if sample_list is None:
        metadata_path = f"{root_path}/sample_sheet.tsv.gz"
        sample_list = list(df_all_samples[group_by].unique())
        SAMPLE_LIST = "*".join(sorted(sample_list))
    else:
        SAMPLE_LIST = "*".join(sorted(sample_list))
        metadata_path = (
            f"{root_path}/scripts/sample_sheet_{group_by}_{SAMPLE_LIST}.tsv.gz"
        )
        df_all_samples[df_all_samples[group_by].isin(sample_list)].to_csv(
            metadata_path, sep="\t", compression="gzip", index=0
        )

    script_name = (
        f"{root_path}/scripts/generate_bulk_bigwig_{source}_{group_by}_{SAMPLE_LIST}.py"
    )

    if source == "met":
        if step_size is None:
            step_size = 500
    elif source == "acc":
        if step_size is None:
            step_size = 200
    else:
        raise ValueError("source must be acc or met")

    if scenario == "all":
        script = f"""
from methyltree  import help_functions as hf
data_path='{root_path}'
print(data_path)
hf.generate_bulk_data(data_path,source='{source}',min_cells='{min_cells}',group_by='{group_by}',metadata_path='{metadata_path}')
hf.generate_bigwig(data_path,source='{source}',group_by='{group_by}',sample_list='{SAMPLE_LIST}',step_size={step_size},reference='{reference}')
        """

    if scenario == "only_bulk":
        script = f"""
from methyltree  import help_functions as hf
data_path='{root_path}'
print(data_path)
hf.generate_bulk_data(data_path,source='{source}',min_cells='{min_cells}',group_by='{group_by}',metadata_path='{metadata_path}')
        """

    if scenario == "only_bigwig":
        script = f"""
from methyltree  import help_functions as hf
data_path='{root_path}'
print(data_path)
hf.generate_bigwig(data_path,source='{source}',group_by='{group_by}',sample_list='{SAMPLE_LIST}',step_size={step_size},reference='{reference}')
        """

    with open(script_name, "w") as w:
        w.write(script)

    return script_name


def generate_bigwig_core(
    input_dir, outdir, root_dir, source="met", sample_list=None, reference="mm10"
):
    if source == "met":
        step_size = 500
        min_rate_bigwig = 10
    elif source == "acc":
        step_size = 200
        min_rate_bigwig = 5
    else:
        raise ValueError("source must be acc or met")

    genome_size_ref = f"{source_script_dir}/reference/{reference}_genome.size"

    if sample_list is None:
        all_paths = sorted(glob.glob(f"{input_dir}/*.tsv.gz"))
        sample_list = [x.split("/")[-1].split(".tsv.gz")[0] for x in all_paths]

    print("sample list:", sample_list)
    for sample in sample_list:
        print(f"current sample: {sample}")
        command = f"cd {source_script_dir}/Rscripts; Rscript pseudobulk/create_bigwig_pseudobulk_SW.R --indir {input_dir} --outdir {outdir} \
        --bedGraphToBigWig /soft/bio/bedGraphToBigWig-2.8-bbi4/bedGraphToBigWig  --step_size {step_size}  --min_rate_bigwig {min_rate_bigwig} \
         --basedir {root_dir}  --samples {sample}  --genome_size_ref {genome_size_ref}"
        os.system(command)


def generate_bigwig(
    root_dir,
    source="acc",
    group_by="lineage",
    sample_list=None,
    step_size=None,
    reference="mm10",
):
    """
    sample_list: a string of samples joined by '*', like 'A*B*C'
    """

    if source == "met":
        input_dir = f"{root_dir}/met/cpg_level/pseudobulk/{group_by}"
        outdir = f"{root_dir}/met/bigwig"
        if step_size is None:
            step_size = 500
        min_rate_bigwig = 10
    elif source == "acc":
        input_dir = f"{root_dir}/acc/gpc_level/pseudobulk/{group_by}"
        outdir = f"{root_dir}/acc/bigwig"
        if step_size is None:
            step_size = 200
        min_rate_bigwig = 5
    else:
        raise ValueError("source must be acc or met")

    if sample_list is None:
        all_paths = sorted(glob.glob(f"{input_dir}/*.tsv.gz"))
        sample_list = [x.split("/")[-1].split(".tsv.gz")[0] for x in all_paths]
    else:
        sample_list = sample_list.split("*")

    genome_size_ref = f"{source_script_dir}/reference/{reference}_genome.size"
    print(f"genome ref path: {genome_size_ref}")

    print("sample list:", sample_list)
    for sample in sample_list:
        print(f"current sample: {sample}")
        command = f"cd {source_script_dir}/Rscripts; Rscript pseudobulk/create_bigwig_pseudobulk_SW.R --indir {input_dir} --outdir {outdir} \
        --bedGraphToBigWig /soft/bio/bedGraphToBigWig-2.8-bbi4/bedGraphToBigWig  --step_size {step_size}  --min_rate_bigwig {min_rate_bigwig} \
         --basedir {root_dir}  --samples {sample} --genome_size_ref {genome_size_ref}"
        os.system(command)


def generate_differential_analysis_script(
    annotation_list, root_dir, metadata_path=None
):
    if metadata_path is None:
        metadata_path = f"{root_dir}/sample_sheet.tsv.gz"

    script_list = []
    for anno_tmp in annotation_list:
        script_name = f"{root_dir}/scripts/diff_analysis_{anno_tmp}.py"
        script = f"""
from methyltree  import help_functions as hf
import pandas as pd
data_path='{root_dir}'
print(data_path)
df_sample=pd.read_csv('{metadata_path}',sep='\t',compression='gzip')
selected_fates=list(set(df_sample['lineage']))
selected_fates.remove('nan0')
print(selected_fates)
hf.differential_analysis(data_path,selected_fates,anno='{anno_tmp}',source='acc',min_cell_N=5,min_C_count=5,metadata_path='{metadata_path}')
hf.differential_analysis(data_path,selected_fates,anno='{anno_tmp}',source='met',min_cell_N=5,min_C_count=3,metadata_path='{metadata_path}')
        """
        with open(script_name, "w") as w:
            w.write(script)
        script_list.append(script_name)
    return script_list


def run_sbatch(
    command,
    sbatch_mode="intel-sc3",
    mem="10G",
    cores=2,
    time="01:0:0",
    job_name="sbatch",
):
    os.system("mkdir -p log")
    sbatch_command = f'sbatch -p {sbatch_mode} -c {cores} -t {time} --mem={mem} --job-name {job_name} --output=log/{job_name}-%j.o  --error=log/{job_name}-%j.e --mail-type=TIME_LIMIT_90,FAIL,END --wrap="{command}"'
    print(f"submit job:   {sbatch_command}")
    os.system(sbatch_command)


def merge_fastq(data_path_1, data_path_2, data_path_out, SampleList):
    """
    Merge fastq files from different sequencing run
    ```python
    import yaml
    import os
    root_dir='/storage/wangshouwenLab/wangshouwen/DATA/multiomics/20211027_scLimeCat_LARRY'
    with open(f"{root_dir}/result_DNA_merged/config.yaml", "r") as stream:
        file = yaml.safe_load(stream)
        SampleList_DNA = file["SampleList"]

    data_path_1=f'{root_dir}/raw_fastq'
    data_path_2=f'{root_dir}/reseq_data/raw_fastq'
    data_path_out=f'{root_dir}/merge/raw_fastq'

    merge_fastq(data_path_1,data_path_2,data_path_out,SampleList)
    ```
    """

    for sample in tqdm(SampleList):
        os.makedirs(f"{data_path_out}/{sample}", exist_ok=True)
        # os.system(f'rm {data_path}/{sample}_R1_001.fastq.gz')
        for source in ["R1", "R2"]:
            file_1 = f"{data_path_1}/{sample}/{sample}_{source}.fastq.gz"
            file_2 = f"{data_path_2}/{sample}/{sample}_{source}.fastq.gz"
            file_3 = f"{data_path_out}/{sample}/{sample}_{source}.fastq.gz"
            if os.path.exists(file_1) & os.path.exists(file_2):
                command = f"cat {file_1} {file_2}   > {file_3}"
                os.system(command)
                # hf.run_sbatch(command,mem='15G',cores=1,time='00:15:00',job_name=f'cat_{sample}_{source}')
            elif os.path.exists(file_1) and (not os.path.exists(file_2)):
                print(f"{sample} not exist in data_path_2. Direct copy")
                os.system(f"cp {file_1} {file_3}")
            elif os.path.exists(file_2) and (not os.path.exists(file_1)):
                print(f"{sample} not exist in data_path_1. Direct copy")
                os.system(f"cp {file_2} {file_3}")
            else:
                print(f"{sample} not exist in either data_path_1 or data_path_2")


def generate_bulk_data(
    root_dir,
    source="acc",
    min_cells=2,  # 5
    ncores=1,
    group_by="lineage",
    metadata_path=None,
):
    # log_dir=f'{root_dir}/log'
    # os.makedirs(log_dir,exist_ok=True)

    # metadata=f"{root_dir}/results/met/qc/sample_metadata_after_met_qc.txt.gz"
    if metadata_path is None:
        metadata_path = f"{root_dir}/sample_sheet.tsv.gz"
    if source == "met":
        input_dir = f"{root_dir}/met/cpg_level"
        outdir = f"{root_dir}/met/cpg_level/pseudobulk/{group_by}"
        context = "CG"
    elif source == "acc":
        input_dir = f"{root_dir}/acc/gpc_level"
        outdir = f"{root_dir}/acc/gpc_level/pseudobulk/{group_by}"
        context = "GC"
    else:
        raise ValueError("source must be acc or met")

    command = f"cd {source_script_dir}/Rscripts; Rscript pseudobulk/pseudobulk_metacc_SW.R --indir {input_dir} --metadata {metadata_path} --context {context} --group_by {group_by} \
        --ncores {ncores} --min_cells {min_cells} --outdir {outdir} --basedir {root_dir}"
    os.system(command)


def differential_analysis(
    root_dir: str,
    selected_fates: list,
    anno: str,
    source="acc",
    min_cell_N=5,
    min_C_count=5,
    metadata_path=None,
):
    """
    root_dir:
        directory to downstream_R/all_data
    selected_fates:
        A list of selected fates to perform differential analysis
    anno:
        annotation
    min_cell_N:
        minimum number of cells per group
    min_C_count:
        minimum C counts per cell per feature
    """
    if metadata_path is None:
        metadata_path = f"{root_dir}/sample_sheet.tsv.gz"
    if source == "met":
        data_dir = f"{root_dir}/met/feature_level"
    elif source == "acc":
        data_dir = f"{root_dir}/acc/feature_level"
    else:
        raise ValueError("source must be acc or met")

    all_files = [x for x in os.listdir(data_dir) if x.endswith(".tsv.gz") and anno in x]
    if len(all_files) == 0:
        raise ValueError(f"The selected annotation {anno} has not been computed yet")

    sel_N = len(selected_fates)
    for j in range(sel_N):
        for k in range(j + 1, sel_N):
            lineage_1 = selected_fates[j]
            lineage_2 = selected_fates[k]

            file_name = "*".join(sorted([lineage_1, lineage_2]))
            test_method = "binomial"  # binomial or t_test
            outfile = f"{root_dir}/{source}/differential/{anno}*{file_name}.txt"
            os.makedirs(os.path.dirname(outfile), exist_ok=True)
            if source == "acc":
                script = (
                    f"{source_script_dir}/diff/differential_analysis_acc.R"
                )
            else:
                script = (
                    f"{source_script_dir}/diff/differential_analysis_met.R"
                )
            os.system(
                f"""Rscript {script}   --data_dir {data_dir}  --sample_file {metadata_path}  --anno {anno}  --lineage1 {lineage_1} --lineage2 {lineage_2}    --min_cells {min_cell_N}  --min_C_count {min_C_count}  --outfile {outfile}   --test_method {test_method}"""
            )
