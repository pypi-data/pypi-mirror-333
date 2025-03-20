import time

import numpy as np
import scipy.sparse as ssp
from matplotlib import pyplot as plt
from tqdm import tqdm

from .settings import *


def compute_similarity_matrix(
    input_X_orig,
    method="correlation",
    cores=64,
):
    """
    Calculate the similarity matrix by explicitly excluding entries with NAN

    When computing similarity between two cells, only use the features detected
    in both cells to calculate the result.

    Parameters
    ---------
        input_X:
            cell (N) by feature (M) matrix, a numpy array
        method:
            Method to compute the similarity. Currently only support "correlation", "correlation_fast".
            correlation_fast is also an exact method.

    Returns
    -------
        corr:
            The similarity matrix

    """
    print(f"Use {method} for similarity")
    start = time.time()
    from scipy.stats import spearmanr

    def spearman_corr(X, Y):
        correlation, p_value = spearmanr(X, Y)
        return correlation

    def pearson_corr(X, Y):
        return np.corrcoef(X, Y)[0, 1]

    def jaccard_similarity(X, Y):
        matches = np.sum(X == Y)
        return matches / len(X)

    def manhattan_similarity(X, Y):
        return 1 - np.sum(np.abs(X - Y)) / len(X)

    ## Most of these methods only support binary data format. Also, these methods are not compatible with our similarity correction method
    method_dict = {
        "correlation": pearson_corr,
        "jaccard": jaccard_similarity,
        "manhattan": manhattan_similarity,
        "spearman": spearman_corr,
    }

    N = input_X_orig.shape[0]
    M = input_X_orig.shape[1]
    shared_site_matrix = np.zeros((N, N))

    if method != "correlation_fast":
        # use a soft-link, because we will not modify input_X in this method
        if method not in method_dict.keys():
            raise ValueError(
                f"method should be among {method_dict.keys()}, but has the value {method}"
            )

        input_X = input_X_orig

        non_nan_matrix = ~np.isnan(input_X)
        # X_similarity = np.zeros((N, N))

        def compute_similarity_core(i):
            X_similarity_vector = np.zeros(N)
            shared_site_matrix_vector = np.zeros(N)
            for j in range(i + 1, N):
                joint_non_nan_index = non_nan_matrix[i] & non_nan_matrix[j]
                X = input_X[i][joint_non_nan_index]
                Y = input_X[j][joint_non_nan_index]
                X_similarity_vector[j] = method_dict[method](X, Y)
                shared_site_matrix_vector[j] = np.sum(joint_non_nan_index)
            return X_similarity_vector, shared_site_matrix_vector

        from joblib import Parallel, delayed

        results = Parallel(n_jobs=cores)(
            delayed(compute_similarity_core)(_) for _ in range(N)
        )
        X_similarity = np.array([x[0] for x in results])
        shared_site_matrix = np.array([x[1] for x in results])

        X_similarity = X_similarity + X_similarity.T
        diag_index = np.diag(np.ones(X_similarity.shape[0])) > 0
        X_similarity[diag_index] = 1
        mask = np.zeros_like(X_similarity, dtype=bool)
        mask[np.triu_indices_from(X_similarity, k=1)] = True

        NaN_num = np.sum(np.isnan(X_similarity))
        if NaN_num > 0:
            print(
                f"Warn: {NaN_num} NaN generated in X_similarity, filled with global mean"
            )
            tru_mean = X_similarity[~np.isnan(X_similarity)].mean()
            X_similarity = np.nan_to_num(X_similarity, nan=tru_mean)

    elif method == "correlation_fast":
        # make a copy so that we can modify this input_X
        if ssp.issparse(input_X_orig):
            input_X = input_X_orig.A.copy()
        else:
            input_X = input_X_orig.copy()

        non_nan_matrix = ~np.isnan(input_X)
        non_nan_count = (~non_nan_matrix).sum()

        if non_nan_count > 0:
            # after zero-centering, correlation becomes cosine similarity.
            # Note that here we use the mean of the entire vector from a cell, rather than using
            # only the shared region with another cell j to compute the mean.
            # This is the only difference with the exact/slow method
            # the assumption is that this global mean and local mean within the shared regions should be rather similar
            print("-------zero centered--------")
            for x in range(N):
                tmp = input_X[x]
                input_X[x] = tmp - np.mean(tmp[~np.isnan(tmp)])

            input_X = np.nan_to_num(
                input_X, nan=0
            )  # by replacing nan with zero, the dot product below only considers values with non-zero entries between two cells.
            cosine_dot_product = input_X.dot(input_X.T)

            # compute the pair-wise normalization factor. Need to consider regions detected in both cells
            X_square = input_X * input_X  # used for normalization
            norm_array = np.ones((N, N))

            for i in tqdm(range(N)):
                for j in range(i + 1, N):
                    # use the boolean vector, and summation. This is computationally cheaper than multiplication
                    joint_non_nan_index = non_nan_matrix[i] & non_nan_matrix[j]
                    norm_array[i, j] = np.sum(X_square[i][joint_non_nan_index])
                    norm_array[j, i] = np.sum(X_square[j][joint_non_nan_index])
                    shared_site_matrix[i, j] = np.sum(joint_non_nan_index)

            X_similarity = cosine_dot_product / np.sqrt(norm_array * norm_array.T)
            diag_index = np.diag(np.ones(X_similarity.shape[0])) > 0
            X_similarity[diag_index] = 1
        else:
            X_similarity = fast_pearson_correlation_between_matrix_without_NaN(
                input_X, input_X
            )

    shared_site_matrix = shared_site_matrix + shared_site_matrix.T
    end = time.time()
    print(f"duration: {end-start}")

    return X_similarity, shared_site_matrix


def correct_similarity_matrix(
    X_similarity_old,
    fig_out=True,
    method="fast",
    epsilon=0.01,
    lower_cutoff=0.4,
    upper_cutoff=2.5,
):
    """
    We assume that X_similarity is a square matrix
    """

    if method == "fast":
        print("Use fast/analytical correction method")
    else:
        print("Use old/slow correction method")

    def cost(similarity_matrix):
        tmp = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]
        return np.std(tmp) / np.mean(tmp)

    def weight_rescaling(weight):
        # mean-center before thresholding. Rescaling the weight does the change our cost function
        # but it affects the similarity, and improves the final result
        weight = weight / np.mean(weight)
        return weight

    def compute_increment_for_current_cell(j0):
        weight_vector_tmp = weight_vector.copy()
        weight_vector_tmp[j0] = (
            weight_vector_tmp[j0] + epsilon
        )  # *(np.random.randint(2)[0]-1)
        weight_matrix_tmp = (
            weight_vector_tmp[:, np.newaxis] * weight_vector_tmp[np.newaxis, :]
        )

        weighted_X_similarity_tmp = X_similarity_old * weight_matrix_tmp
        std_1d_tmp = cost(weighted_X_similarity_tmp)
        return -(std_1d_tmp - std_1d_new)

    ## initialize the weight vector
    max_values = []
    for i in range(X_similarity_old.shape[0]):
        vector_drop_diag = np.hstack(
            [X_similarity_old[i, :i], X_similarity_old[i, (i + 1) :]]
        )
        max_values.append(abs(vector_drop_diag.max()))

    weight_vector = weight_rescaling(1 / np.sqrt(np.array(max_values)))

    std_history = [1000]
    weight_vector_history = [weight_vector]

    weight_matrix_initial = weight_vector[:, np.newaxis] * weight_vector[np.newaxis, :]
    weighted_X_similarity = X_similarity_old * weight_matrix_initial
    std_1d_new = cost(weighted_X_similarity)
    std_history.append(std_1d_new)
    weight_vector_history.append(weight_vector)

    diff = np.zeros(len(weight_vector))
    for _ in tqdm(range(1000)):
        ## compute the optimal direction of improvement. This mitigates the risk of overfitting
        if method == "fast":
            S_old = X_similarity_old.copy()
            S_new = weighted_X_similarity.copy()
            N0 = S_old.shape[0]
            norm_factor = N0 * (N0 - 1) / 2
            np.fill_diagonal(S_old, np.nan)
            np.fill_diagonal(S_new, np.nan)

            S_new_std = np.nanstd(S_new.flatten())
            S_new_mean = np.nanmean(S_new.flatten())
            diff_X = S_old * (weight_vector[:, np.newaxis])

            dY_dz = np.nansum((S_new - S_new_mean) * (diff_X), axis=0) * 2 / norm_factor
            dX_dz = np.nansum(diff_X, axis=0) / (norm_factor)
            diff_analytic = (
                1 / (2 * S_new_std * S_new_mean) * dY_dz
                - S_new_std / (S_new_mean * S_new_mean) * dX_dz
            )
            diff = -diff_analytic
        else:
            for j in np.arange(len(weight_vector)):
                diff[j] = compute_increment_for_current_cell(j)

        ## update the weight vector, and compute the new similarity
        weight_vector = weight_rescaling(
            weight_vector + epsilon * diff / np.max(abs(diff))
        )
        weight_vector_history.append(weight_vector)

        weight_matrix = weight_vector[:, np.newaxis] * weight_vector[np.newaxis, :]
        weighted_X_similarity = X_similarity_old * weight_matrix
        std_1d_new = cost(weighted_X_similarity)
        std_history.append(std_1d_new)

        ## check convergence and then exit
        excess_weight = (np.sum(weight_vector >= upper_cutoff) > 0) or (
            np.sum(weight_vector <= lower_cutoff) > 0
        )
        if (std_1d_new >= std_history[-2]) or excess_weight:
            break

    weight_vector = weight_vector_history[np.argmin(std_history)]
    weight_matrix = weight_vector[:, np.newaxis] * weight_vector[np.newaxis, :]
    weight_X_similarity = X_similarity_old * weight_matrix
    X_similarity = weight_X_similarity

    if fig_out:
        plt.subplots(figsize=(4, 3.5))
        plt.plot(
            np.arange(len(weight_vector)),
            weight_vector_history[0],
            ".",
            label="initial",
        )
        plt.plot(np.arange(len(weight_vector)), weight_vector, ".", label="final")
        plt.ylim([0, 2])
        plt.xlabel("Cell order")
        plt.ylabel("Weight")
        plt.legend()
        plt.show()

        # std_history = np.array(std_history)
        # plt.subplots(figsize=(4, 3.5))
        # plt.plot(np.arange(len(std_history) - 1), std_history[1:], ".")
        # plt.xlabel("Iteration")
        # plt.ylabel("Std/mean")

        off_diag_idx = ~(np.diag(np.ones(X_similarity_old.shape[0])) > 0)
        temp_X_orig = weight_matrix_initial[off_diag_idx].flatten()
        if len(temp_X_orig) > 5000:
            sel_idx = np.random.choice(np.arange(len(temp_X_orig)), 5000)
        else:
            sel_idx = np.arange(len(temp_X_orig))
        plt.subplots(figsize=(4, 3.5))
        plt.plot(
            temp_X_orig[sel_idx],
            X_similarity_old[off_diag_idx].flatten()[sel_idx],
            ".b",
        )
        plt.xlabel("1/sqrt(max_i*max_j)")
        plt.ylabel("Similarity")
        plt.title("Original")
        plt.show()

        # plt.subplots(figsize=(4, 3.5))
        # plt.plot(
        #     temp_X_orig[sel_idx],
        #     X_similarity[off_diag_idx].flatten()[sel_idx],
        #     ".r",
        # )
        # plt.xlabel("1/sqrt(max_i*max_j)")
        # plt.ylabel("Similarity")
        # plt.title("New")
        # plt.show()

    return X_similarity


def remove_celltype_signal_discrete_state(
    X_similarity,
    cell_type_array,
    outlier_threshold=1,
):
    """
    Cell-specific zscore.

    S=T+L
    Here, we calcualte the cell-specific T_ij.  Assume that i belongs to type p, and j to q.
    mean_T_i: mean similarity between i and all cells with type q (from j)
    mean_T_j: mean similarity between j and all cells with type p (from i)
    Then, compute the mean: T_ij=(mean_T_i+mean_T_j)/2

    This method proves to be more accurate than just using the mean similarity
    between all cells from type p and type q.

    outlier_threshold=1
    A smaller outlier_threshold excludes more cells.
    A very large outlier_threshold means that nothing is excluded.

    Remove the diagonal effect, and the outliers, proves to be useful.
    """

    unique_cell_types = list(set(cell_type_array))

    mean_matrix = np.zeros(X_similarity.shape)
    all_values = X_similarity[np.triu_indices(X_similarity.shape[0], k=1)]
    global_mean = np.mean(all_values)

    for i in range(len(unique_cell_types)):
        for j in range(i, len(unique_cell_types)):
            x = unique_cell_types[i]
            y = unique_cell_types[j]

            sel_index_1 = np.nonzero(cell_type_array == x)[0]
            sel_index_2 = np.nonzero(cell_type_array == y)[0]

            X_sub = X_similarity[sel_index_1][:, sel_index_2].copy()
            values = X_sub.flatten()

            # remove cell-pairs with abnormally high similarity (due to lineage similarity)
            # This improves the result.
            cutoff_tmp_high = np.mean(values) + outlier_threshold * np.std(values)
            X_sub[(X_sub > cutoff_tmp_high)] = np.nan

            if i == j:
                np.fill_diagonal(X_sub, np.nan)
                X0 = np.nanmean(X_sub, axis=0, keepdims=True)
                X_mean = (X0 + X0.T) / 2
            else:
                X0 = np.nanmean(X_sub, axis=0, keepdims=True)
                X1 = np.nanmean(X_sub, axis=1, keepdims=True)
                X_mean = (X0 + X1) / 2

            mean_matrix[np.ix_(sel_index_1, sel_index_2)] = X_mean
            mean_matrix[np.ix_(sel_index_2, sel_index_1)] = X_mean.T

    mean_matrix[np.isnan(mean_matrix)] = global_mean
    new_S_matrix = X_similarity - mean_matrix
    np.fill_diagonal(new_S_matrix, 1)

    return new_S_matrix


def remove_celltype_signal_continuous_state(
    X_similarity, neighbor_info, outlier_threshold=1
):
    all_values = X_similarity[np.triu_indices(X_similarity.shape[0], k=1)]
    global_mean_x = np.mean(all_values)
    mean_matrix = np.zeros(X_similarity.shape)

    for i in range(X_similarity.shape[0]):
        for j in range(i, X_similarity.shape[0]):
            index_list = [i, j]
            mean_value_list = []
            for _ in index_list:
                sel_index_1 = np.array(neighbor_info[_])
                if i == j:
                    sel_index_2 = sel_index_1
                    # This part is different from the fast method. But it only affects the diagonal
                    # And the diagonal is eventually set to be 1
                else:
                    tmp = index_list.copy()
                    tmp.remove(_)
                    sel_index_2 = [tmp[0]]

                if _ == i:
                    X_sub = X_similarity[sel_index_1][:, sel_index_2]
                else:
                    X_sub = X_similarity[sel_index_2][:, sel_index_1]

                if i == j:
                    values = X_sub[np.triu_indices(X_sub.shape[0], k=1)]
                else:
                    values = X_sub.flatten()

                # remove cell-pairs with abnormally high similarity (due to lineage similarity)
                cutoff_tmp_high = np.mean(values) + outlier_threshold * np.std(values)
                mean_value = np.mean(values[(values < cutoff_tmp_high)])
                mean_value_list.append(mean_value)

            mean_matrix[i, j] = np.mean(mean_value_list)
            mean_matrix[j, i] = mean_matrix[i, j]

    mean_matrix[np.isnan(mean_matrix)] = global_mean_x
    new_S_matrix = X_similarity - mean_matrix
    np.fill_diagonal(new_S_matrix, 1)
    return new_S_matrix


def rescale_similarity_matrix(X_similarity):
    temp_array = X_similarity[np.triu_indices_from(X_similarity, k=1)]
    min_value = temp_array.min()
    max_value = temp_array.max()
    # add a max weight 0.999, so that only the diagonal will be 1
    X_similarity_new = 0.999 * (X_similarity - min_value) / (max_value - min_value)
    np.fill_diagonal(X_similarity_new, 1)
    return X_similarity_new


def fast_pearson_correlation_between_matrix_without_NaN(x, y):
    """
    compute the correlation along the axis=1.
    So, if x has the shape: n1*M
           y has the shape: n2:M
        Then, the result has the shape: n1*n2
    """
    x1 = x.transpose()
    y1 = y.transpose()
    xv = x1 - x1.mean(axis=0)
    yv = y1 - y1.mean(axis=0)
    xvss = (xv * xv).sum(axis=0)
    yvss = (yv * yv).sum(axis=0)
    result = np.matmul(xv.transpose(), yv) / np.sqrt(np.outer(xvss, yvss))
    # bound the values to -1 to 1 in the event of precision issues
    return (result + result.T) / 2
