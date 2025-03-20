import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

def normalized_clustering_quality_index(X, labels, alpha=1.5):
    unique_labels = np.unique(labels)
    k = len(unique_labels)
    if k <= 1:
        return 0

    cluster_centers = np.array([X[labels == label].mean(axis=0) for label in unique_labels])

    # محاسبه انسجام (Cohesion)
    cohesion = np.mean([
        np.mean(euclidean_distances(X[labels == label], [cluster_centers[i]]))
        for i, label in enumerate(unique_labels)
    ])

    # محاسبه جدایی (Separation)
    separation_matrix = euclidean_distances(cluster_centers)
    np.fill_diagonal(separation_matrix, 0)
    separation = np.sum(separation_matrix) / (k * (k - 1))

    # محاسبه نهایی شاخص NCQI
    ncqi = separation / (alpha * cohesion + separation)
    return np.clip(ncqi, 0, 1)
