import numpy as np
from sklearn.neighbors import NearestNeighbors

def calculate_distances_close(X, p, close):
    """
    Efficiently calculates the average distance to the closest 'close' points for each point in the dataset.

    Parameters:
    X : np.ndarray
        The dataset (n_samples, n_features).
    p : int
        The norm for the Minkowski distance.
    close : int
        The number of nearest points to consider.

    Returns:
    np.ndarray
        Average distances array.
    """
    n_samples = X.shape[0]
    if n_samples <= 1:
        return np.zeros(n_samples)
    
    k_neighbors = min(close + 1, n_samples)
    nn = NearestNeighbors(n_neighbors=k_neighbors, algorithm='auto', p=p)
    nn.fit(X)
    distances, _ = nn.kneighbors(X)
    
    if n_samples - 1 >= close:
        neighbor_distances = distances[:, 1:close+1]
    else:
        neighbor_distances = distances[:, 1:]
    
    return np.mean(neighbor_distances, axis=1)

def _classify_border_and_core_points(X, p=2, close=100, percentile=60):
    """
    Classifies points into border and core based on distance percentiles.

    Parameters:
    X : np.ndarray
        Input dataset.
    p : int
        Minkowski distance parameter.
    close : int
        Number of closest neighbors considered.
    percentile : float
        Percentile threshold for classification.

    Returns:
    tuple of np.ndarray
        Border and core points arrays.
    """
    distances = calculate_distances_close(X, p, close)
    threshold = np.percentile(distances, percentile)
    
    border_mask = distances >= threshold
    core_mask = ~border_mask
    
    border_points = X[border_mask]
    core_points = X[core_mask]
    
    # Sorting by distances
    border_points = border_points[np.argsort(-distances[border_mask])]
    core_points = core_points[np.argsort(distances[core_mask])]
    
    return border_points, core_points

def classify_border_and_core_points(X, y=None, p=2, close=100, percentile=60):
    """
    Classify points as 'border' or 'core' based on distance percentile, using efficient distance computation.
    
    Parameters:
    X : np.ndarray
        The dataset (n_samples, n_features).
    y : np.ndarray, optional
        The class labels for the dataset (n_samples,). If None, the function treats all data as one class.
    p : int
        The norm to use for distance calculation (default is Euclidean norm, p=2).
    close : int
        The number of closest points to consider for the distance calculation (default=100).
    percentile : float
        The threshold percentile for defining border points (default=60).
    
    Returns:
    result : dict or tuple
        If y is provided, returns a dictionary with class labels as keys and (border_points, core_points) as values.
        If y is None, returns a tuple (border_points, core_points).
    """
    
    if y is None:
        return _classify_border_and_core_points(X)
        
    unique_classes = np.unique(y)
    class_border_core = {}
    
    for cls in unique_classes:
        mask = (y == cls)
        X_cls = X[mask]
        border, core = _classify_border_and_core_points(X_cls, p, close, percentile)
        class_border_core[cls] = (border, core)
    
    return class_border_core
