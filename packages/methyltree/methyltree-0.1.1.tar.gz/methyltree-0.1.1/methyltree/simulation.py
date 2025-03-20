import os
import random
import time

import numpy as np
import scanpy as sc
import scipy.sparse as ssp
from tqdm import tqdm


def select_remaining_values(value):
    remaining_values = [0, 1]
    if value in remaining_values:
        remaining_values.remove(value)
    selected_value = random.choice(remaining_values)
    return selected_value


def mutation_sequence(sequence, mutation_rate):
    new_sequence = sequence.copy()
    selected_sites = np.nonzero(np.random.rand(len(new_sequence)) < mutation_rate)[0]
    for i_site in selected_sites:
        new_sequence[i_site] = select_remaining_values(new_sequence[i_site])
    return new_sequence


def sigma(x, diff_sigma):
    #    return 0.1*np.sin(0.1*x)+0.1
    return diff_sigma


def progression(x, dL):
    #    return 0.1*np.sin(0.1*x)+1
    return dL


def transition_prob(x, y_vec, diff_sigma, dL):
    temp = []
    for y in y_vec:
        temp.append(
            np.exp(
                -((x - y + progression(x, dL)) ** 2) / (2 * (sigma(x, diff_sigma) ** 2))
            )
        )

    norm_Prob = np.array(temp) / np.sum(temp)

    return norm_Prob


def simulate_replication_next_time_point(
    x_input_list, cell_name_list_input, mutation_rate=0.01, progeny_N=2
):
    x_next_list = []
    cell_name_list_new = []

    for j, sequence in enumerate(x_input_list):
        old_name = cell_name_list_input[j]

        for k in range(progeny_N):
            new_sequence = sequence.copy()
            CpG_size = len(sequence)

            # mutate the CpG sites
            new_sequence = mutation_sequence(new_sequence, mutation_rate)

            x_next_list.append(new_sequence)
            cell_name_list_new.append(f"{old_name}-{k}")

    return x_next_list, cell_name_list_new


def simulate_discrete_differentiation_next_time_point(
    x_input_list,
    cell_name_list_input,
    mutation_rate=0.01,
    fate_CpG_frac=0.5,
    differentiation_prob=0.3,
    progeny_n=2,
):
    x_next_list = []
    cell_name_list_new = []

    for j, X in enumerate(x_input_list):
        old_name = cell_name_list_input[j]
        sequence = X[0]
        fate = X[1]

        # replication
        for k in range(progeny_n):
            new_sequence = sequence.copy()
            CpG_size = sequence.shape[0]

            # update fate in a probabilistic way
            if fate != -1:
                new_fate = fate  # already differentiated, keep the same fate
            else:
                if np.random.rand(1) < differentiation_prob:
                    new_fate = int(
                        np.random.rand(1) > 0.5
                    )  # choose fate between 0 and 1
                else:
                    new_fate = -1  # keep the un-differentiated fate

            # effect of differentiation on the CpG state
            if fate != new_fate:
                end_CpG = int(fate_CpG_frac * CpG_size)
                new_sequence[:end_CpG] = new_fate  # B branch

            # mutate the CpG sites
            new_sequence = mutation_sequence(new_sequence, mutation_rate)

            x_next_list.append([new_sequence, new_fate])
            cell_name_list_new.append(f"{old_name}-{k}")

    return x_next_list, cell_name_list_new


def simulate_bifurcation_next_time_point(x_input_list, cell_name_list, parameter):
    rna_diff_length = parameter["rna_diff_length"]
    rna_dL = parameter["rna_dL"]
    diff_sigma = parameter["diff_sigma"]
    progeny_N = parameter["progeny_N"]
    lattice = parameter["lattice"]
    bifurcation = parameter["bifurcation"]
    mutation_rate = parameter["mutation_rate"]
    fate_CpG_frac = parameter["fate_CpG_frac"]

    x_next_list = []
    cell_name_list_new = []

    for j, X in enumerate(x_input_list):
        old_name = cell_name_list[j]
        x = X[0]
        sequence = X[1]
        fate = X[2]
        ## this method is much faster
        if x < rna_diff_length - (
            1.5 * progression(x, rna_dL) + 5 * sigma(x, diff_sigma)
        ):
            new_x_list = np.random.normal(
                x + progression(x, rna_dL), sigma(x, diff_sigma), progeny_N
            )

        else:
            ## this method is much slower
            new_x_list = []
            for k in range(progeny_N):
                cum_Prob = np.cumsum(transition_prob(x, lattice, diff_sigma, rna_dL))
                # pick the first event that is larger than the random variable
                new_id = np.nonzero(cum_Prob > np.random.rand())[0][0].astype(int)
                new_x_list.append(lattice[new_id])

        ## loop for each progeny
        for k, new_x in enumerate(new_x_list):
            # update fate
            if x >= bifurcation:  # do not change fate, already committed
                new_fate = fate
            elif (x < bifurcation) and (new_x < bifurcation):
                new_fate = -1
            else:
                new_fate = np.random.randint(2)

            # update the CpG methylation due to changes of cell type
            new_sequence = sequence.copy()
            CpG_size = len(sequence)

            diff_frac_0 = (x - bifurcation) / (rna_diff_length - bifurcation)
            diff_frac_new = (new_x - bifurcation) / (rna_diff_length - bifurcation)

            start_CpG = int(diff_frac_0 * CpG_size * fate_CpG_frac)
            end_CpG = int(diff_frac_new * CpG_size * fate_CpG_frac)

            # already differentiated, modify a new region to indicate differentiation progression
            if (fate == new_fate) and (new_fate != -1) and (end_CpG > start_CpG):
                new_sequence[start_CpG:end_CpG] = new_fate

            # differentiation and fate change
            if (fate != new_fate) and (diff_frac_new >= 0):
                new_sequence[:end_CpG] = new_fate  # B branch

            # mutate the CpG sites
            new_sequence = mutation_sequence(new_sequence, mutation_rate)

            x_next_list.append([new_x, new_sequence, new_fate])
            cell_name_list_new.append(f"{old_name}-{k}")

    return x_next_list, cell_name_list_new


def replication_model(
    CpG_size=10000,
    initial_random_rate=0.05,
    clone_N=1,
    mutation_rate=0.01,
    generation=5,
    sequence_initial_orig=None,
):
    print("Generate new data")
    met_X = []
    met_names = []
    clone_id = []
    # initialize baseline methylation profile, same for all clones
    if sequence_initial_orig is None:
        sequence_initial_orig = (np.random.rand(CpG_size) > 0.5).astype(int)
    for j in range(clone_N):
        sequence_initial = mutation_sequence(sequence_initial_orig, initial_random_rate)

        x_next_list = [sequence_initial]
        cell_name_list = [f"{j}"]
        for _ in range(generation):
            x_next_list, cell_name_list = simulate_replication_next_time_point(
                x_next_list, cell_name_list, mutation_rate=mutation_rate, progeny_N=2
            )
        met_X = met_X + x_next_list
        met_names = met_names + cell_name_list

        clone_id = clone_id + [f"clone_{j}" for _ in range(len(cell_name_list))]

    adata_met = sc.AnnData(np.array(met_X))
    adata_met.obs_names = met_names
    adata_met.obs["clone_id"] = clone_id
    return adata_met


def discrete_differentiation_model(
    CpG_size=10000,
    initial_random_rate=0.05,
    clone_N=1,
    mutation_rate=0.01,
    fate_CpG_frac=0.5,
    differentiation_prob=0.3,
    generation=5,
    sequence_initial_orig=None,
):
    met_X = []
    met_names = []
    clone_id = []
    fate_list = []
    fate_CpG_N = int(fate_CpG_frac * CpG_size)

    # initialize methylation profile of the baseline profile, same for all clones
    if sequence_initial_orig is None:
        sequence_initial_orig = (np.random.rand(CpG_size) > 0.5).astype(
            float
        )  # need to use 'float', otherwise 0.5 will be forced to 0 if we use int structure
    for i in range(fate_CpG_N):
        sequence_initial_orig[i] = i % 2
    fate = -1
    for j in range(clone_N):
        sequence_initial = mutation_sequence(sequence_initial_orig, initial_random_rate)

        x_next_list = [[sequence_initial, fate]]
        cell_name_list = [f"{j}"]
        for _ in range(generation):
            (
                x_next_list,
                cell_name_list,
            ) = simulate_discrete_differentiation_next_time_point(
                x_next_list,
                cell_name_list,
                mutation_rate=mutation_rate,
                differentiation_prob=differentiation_prob,
                progeny_n=2,
                fate_CpG_frac=fate_CpG_frac,
            )
        met_X = met_X + [X[0] for X in x_next_list]
        fate_list = fate_list + [X[1] for X in x_next_list]
        met_names = met_names + cell_name_list

        clone_id = clone_id + [f"clone_{j}" for _ in range(len(cell_name_list))]

    fate_map = {-1: "stem", 0: "diff_A", 1: "diff_B"}
    adata_met = sc.AnnData(np.array(met_X))
    adata_met.obs_names = met_names
    adata_met.obs["clone_id"] = clone_id
    adata_met.obs["fate"] = [fate_map[_] for _ in fate_list]
    return adata_met


def single_cell_expansion(
    CpG_size,
    mutation_rate=0.001,
    generation=7,
    pruning_size=128,
    sequence_initial_orig=None,
):
    met_X = []
    met_names = []
    if sequence_initial_orig is None:
        sequence_initial_orig = (np.random.rand(CpG_size) > 0.5).astype(int)
    sequence_initial = mutation_sequence(
        sequence_initial_orig, mutation_rate
    )  # start from a single cell

    ## the first generation
    x_next_list = [sequence_initial]
    cell_name_list = [f"P0*"]
    for _ in range(generation):
        print(f"current generation: {_}")
        print(f"current cell number: {len(x_next_list)}")
        if len(x_next_list) > pruning_size:
            id_array = np.arange(len(x_next_list))
            sel_id = np.random.choice(id_array, pruning_size)
            x_next_list = np.array(x_next_list)[sel_id]
            cell_name_list = np.array(cell_name_list)[sel_id]
        x_next_list, cell_name_list = simulate_replication_next_time_point(
            x_next_list, cell_name_list, mutation_rate=mutation_rate, progeny_N=2
        )

    met_X = met_X + list(np.array(x_next_list))  # [sel_id])
    met_names = met_names + list(np.array(cell_name_list))  # [sel_id])

    adata_met = sc.AnnData(np.array(met_X))
    adata_met.obs_names = met_names
    adata_met.obs["clone_id"] = ["-".join(x.split("-")[:-3]) for x in met_names]
    return adata_met


def bifurcation_model(
    progeny_N=2,
    generation=5,
    sample_prob=0.5,
    clone_N=50,
    rna_diff_length=10,
    diff_sigma=0.5,
    repeat_N=1,
    rna_dL=1,
    CpG_size=10000,
    initial_random_rate=0.05,
    mutation_rate=0.01,
    re_simulate=False,
    data_dir="simulated_data",
    fate_CpG_frac=0.5,
    mRNA_bifurcation_frac=0.5,
    sequence_initial_orig=None,
):
    """
    Jointly simulate methylation, RNA, and lineage for individual clones in a bifurcation model

    Parameters
    ----------
    progeny_N:
        Fold change of clone size after each generation. 2 means that it will double its clone size after one generation.
    generation:
        Initital sampling time point. Unit: cell cycle. By default
        t2=t1+1.
    sample_prob:
        Probability to sample cells at t1
    clone_N:
        Total number of clones to simulate
    rna_diff_length:
        Total length of the 1-d differentiation manifold
    diff_sigma:
        Differentiation noise
    rna_dL:
        Step size of differentiation for one generation
    re_simulate:
        Simulate new data (do not load pre-saved datasets)

    Returns
    -------
    adata:
        An adata object with clonal matrix, time info etc. Ready to be plugged into CoSpar.
    """

    os.makedirs(data_dir, exist_ok=True)
    file_name = f"{data_dir}/simulated_clonal_data_bifurcation_M{clone_N}_progeny{progeny_N}_L{rna_diff_length}_dL{rna_dL}_diffSigma{diff_sigma}_t1{generation}_p1{sample_prob}_simuV{repeat_N}"

    if os.path.exists(file_name + "_clonal_annot.npz") and (not re_simulate):
        print("Load existing data")
        clone_annot = ssp.load_npz(file_name + "_clonal_annot.npz")
        simu_data = np.load(file_name + "_others.npz", allow_pickle=True)
        rna_X = simu_data["rna_X"]
        met_X = simu_data["met_X"]
        fate_list = simu_data["fate_list"]
        time_info = simu_data["time_info"]
        clone_id = simu_data["clone_id"]
        cell_name_list = simu_data["cell_name_list"]
        bifurcation = mRNA_bifurcation_frac * rna_diff_length

    else:
        print("Generate new data")
        t = time.time()

        # initialize position (RNA) of the founding cell
        n = (
            clone_N * (progeny_N ** (generation + 1)) * 20
        )  # resolution of grid for sampling
        dx = rna_diff_length / n
        lattice = np.linspace(0, rna_diff_length, n)

        max_n = int((rna_diff_length - generation * rna_dL) / dx)
        t0_id = np.sort(
            np.random.choice(max_n, clone_N, replace=False)
        )  # random sample of indices
        x_t0_array = np.array(
            lattice[t0_id]
        )  # position of initial barcoding for each founding cell

        bifurcation = mRNA_bifurcation_frac * rna_diff_length

        parameter = {}
        parameter["rna_diff_length"] = rna_diff_length
        parameter["rna_dL"] = rna_dL
        parameter["diff_sigma"] = diff_sigma
        parameter["progeny_N"] = progeny_N
        parameter["dx"] = dx
        parameter["lattice"] = lattice
        parameter["bifurcation"] = bifurcation
        parameter["mutation_rate"] = mutation_rate
        parameter["fate_CpG_frac"] = fate_CpG_frac

        rna_X = []
        met_X = []
        fate_list = []
        time_info = []
        clone_id = []
        temp_clone_id = 0
        previouse_cell_N = 0
        cell_name_list = []

        # initialize methylation profile of the baseline profile, same for all clones
        if sequence_initial_orig is None:
            sequence_initial_orig = (np.random.rand(CpG_size) > 0.5).astype(
                float
            )  # need to use 'float', otherwise 0.5 will be forced to 0 if we use int structure
        fate_CpG_N = int(fate_CpG_frac * CpG_size)
        sequence_initial_orig[:fate_CpG_N] = 0.5

        ## simulate the multi-generational drift separately for each clone
        for k in tqdm(range(clone_N)):
            x_t0 = x_t0_array[k]
            # print("Current clone number:", m31)
            x_next = []
            cell_name_tmp = [f"{k}"]

            sequence_initial = mutation_sequence(
                sequence_initial_orig, initial_random_rate
            )

            if x_t0 < bifurcation:
                x_next.append([x_t0, sequence_initial, -1])  # fate=-1
            else:
                fate = np.random.randint(2)

                diff_frac = (x_t0 - bifurcation) / (rna_diff_length - bifurcation)
                end_CpG = int(diff_frac * fate_CpG_N)
                sequence_initial[:end_CpG] = fate

                x_next.append([x_t0, sequence_initial, fate])

            for j in range(generation):
                x_next, cell_name_tmp = simulate_bifurcation_next_time_point(
                    x_next, cell_name_tmp, parameter
                )

            sel_idx = np.random.rand(len(x_next)) < sample_prob
            sel_id = list(np.nonzero(sel_idx)[0].astype(int))

            for _ in sel_id:
                rna_X.append(x_next[_][0])
                met_X.append(x_next[_][1])
                fate_list.append(x_next[_][2])
                cell_name_list.append(cell_name_tmp[_])

            time_info = time_info + [1 for _ in range(len(sel_id))]

            clone_id = clone_id + [
                temp_clone_id for _ in range(len(time_info) - previouse_cell_N)
            ]
            previouse_cell_N = len(time_info)
            temp_clone_id = temp_clone_id + 1

        ### Generate clonal data matrix
        clone_annot = np.zeros((len(time_info), len(x_t0_array)))
        for j in range(len(time_info)):
            clone_annot[j, clone_id[j]] = 1

        clone_annot = ssp.csr_matrix(clone_annot)

        ssp.save_npz(file_name + "_clonal_annot.npz", clone_annot)
        np.savez(
            file_name + "_others.npz",
            rna_X=np.array(rna_X),
            met_X=np.array(met_X),
            fate_list=np.array(fate_list),
            time_info=np.array(time_info),
            clone_id=np.array(clone_id),
            cell_name_list=cell_name_list,
        )
        print("Time elapsed for generating clonal data: ", time.time() - t)

    ## transform the RNA data to 50-d
    UMAP_noise = 0.2  #
    rna_X = np.array(rna_X)
    state_info = np.array(fate_list)
    x_2d = np.zeros(len(rna_X))
    y_2d = np.zeros(len(rna_X))
    idx = state_info == -1
    x_2d[idx] = rna_X[idx] - bifurcation
    y_2d[idx] = 0 * rna_X[idx]
    idx = state_info == 0
    x_2d[idx] = 0.5 * (rna_X[idx] - bifurcation)
    y_2d[idx] = 0.5 * (rna_X[idx] - bifurcation)
    idx = state_info == 1
    x_2d[idx] = 0.5 * (rna_X[idx] - bifurcation)
    y_2d[idx] = -0.5 * (rna_X[idx] - bifurcation)

    X_high_dim = np.zeros((len(x_2d), 50))
    X_high_dim[:, 0] = x_2d
    X_high_dim[:, 1] = y_2d

    for j in range(48):
        X_high_dim[:, j + 2] = UMAP_noise * np.random.randn(len(x_2d))

    fate_map = {-1: "stem", 0: "diff_A", 1: "diff_B"}
    adata_rna = sc.AnnData(X_high_dim)
    adata_met = sc.AnnData(np.array(met_X))

    for adata_tmp in [adata_rna, adata_met]:
        adata_tmp.obsm["X_clone"] = clone_annot
        adata_tmp.obs["time_info"] = time_info
        adata_tmp.obs["fate"] = np.array([fate_map[_] for _ in state_info])
        adata_tmp.obsm["X_emb"] = X_high_dim[:, :2]
        adata_tmp.uns["data_des"] = ["bifurcation"]
        adata_tmp.obsm["X_rna_high_da"] = X_high_dim
        adata_tmp.obsm["X_rna_1d"] = rna_X
        adata_tmp.obs["clone_id"] = np.array([f"clone_{_}" for _ in clone_id])
        adata_tmp.obsm["X_met"] = np.array(met_X)
        adata_tmp.obs_names = cell_name_list
        adata_tmp.obs["lineage"] = cell_name_list

    return adata_rna, adata_met
