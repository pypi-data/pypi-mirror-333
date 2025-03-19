This repo provides a single function which is the implementation of the border and core detection as studied in our paper:

The border and core detection function has a prototype as follows.
```py
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
```
# Installation
The code can be installed as a python package from PyPI.
```
pip install adaptive_resampling
```
Or it can be install from the github repo directly as a package.
```
pip install git+https://github.com/ykahalan/adaptive_resampling.git
```

# Example usage
For detecting core and border points of a single class.
```py
# Import the functions from the installed library
from adaptive_resampling import classify_border_and_core_points

# Generate random data points for the example (1000 points in 2D space)
import numpy as np
X = np.random.rand(1000, 2)

# Classify points into border and core points
border_points, core_points = classify_border_and_core_points(X, p=2, close=100, percentile=60)

print(f"Number of border points: {border_points.shape[0]}")
print(f"Number of core points: {core_points.shape[0]}")
```
For detecting core and border points of each class.
```py
# Import the functions from the installed library
from adaptive_resampling import classify_border_and_core_points

# Generate random data points for the example (1000 points in 2D space, with 3 classes)
import numpy as np
np.random.seed(42)
X = np.random.rand(1000, 2)
y = np.random.randint(0, 3, size=1000)  # 3 classes (0, 1, 2)

# Classify border and core points for each class
class_border_core = classify_border_and_core_points(X, y, p=2, close=100, percentile=60)

for cls, (border, core) in class_border_core.items():
    print(f"Class {cls}:")
    print(f"  Number of border points: {border.shape[0]}")
    print(f"  Number of core points: {core.shape[0]}")
```
For oversampling on the border and undersampling on the core as intended in the paper.
```py
# Import necessary libraries
import numpy as np
from adaptive_resampling import classify_border_and_core_points
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter

# Generate synthetic data (1000 samples, 2 features, 3 classes)
np.random.seed(42)
X = np.random.rand(1000, 2)
y = np.random.randint(0, 3, size=1000)  # Classes: 0, 1, 2

# Classify border and core points for each class
class_border_core = classify_border_and_core_points(X, y, p=2, close=100, percentile=60)

# Separate border and core points
border_points = []
border_labels = []
core_points = []
core_labels = []

for cls, (border, core) in class_border_core.items():
    border_points.append(border)
    border_labels.append(np.full(border.shape[0], cls))  # Store labels for border points
    core_points.append(core)
    core_labels.append(np.full(core.shape[0], cls))  # Store labels for core points

# Combine all border points and labels
X_border_all = np.vstack(border_points)
y_border_all = np.hstack(border_labels)

# Combine all core points and labels
X_core_all = np.vstack(core_points)
y_core_all = np.hstack(core_labels)

# Apply SMOTE to all border points across all classes
if len(np.unique(y_border_all)) > 1:  # Ensure multiple classes exist
    smote = SMOTE(sampling_strategy='auto', random_state=42)
    X_border_resampled, y_border_resampled = smote.fit_resample(X_border_all, y_border_all)
else:
    X_border_resampled, y_border_resampled = X_border_all, y_border_all  # Use original if SMOTE isn't possible

# Apply Random Undersampling (RUS) to all core points across all classes
if len(np.unique(y_core_all)) > 1:  # Ensure multiple classes exist
    rus = RandomUnderSampler(sampling_strategy='auto', random_state=42)
    X_core_resampled, y_core_resampled = rus.fit_resample(X_core_all, y_core_all)
else:
    X_core_resampled, y_core_resampled = X_core_all, y_core_all  # Use original if RUS isn't possible

# Combine resampled border and core points
X_resampled = np.vstack((X_border_resampled, X_core_resampled))
y_resampled = np.hstack((y_border_resampled, y_core_resampled))

# Display the class distribution before and after resampling
print(f"Original class distribution: {Counter(y)}")
print(f"Resampled class distribution: {Counter(y_resampled)}")
```
