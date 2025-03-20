# Clustering Evaluation (NCQI)

A Python package for evaluating clustering algorithms using the **Normalized Clustering Quality Index (NCQI)**. This package is designed for researchers and practitioners working with **unsupervised clustering** techniques, providing a **quantitative measure** for cluster quality assessment.

## 📌 Installation
To install the package, run:
```bash
pip install git+https://github.com/Mojtaba-jahanian/Cosine-Clustering-Index-CCI-.git
```

## 📖 Reference Paper
This implementation is based on the research paper:
🔗 ["Cosine Clustering Index (CCI) for Deep Clustering Evaluation"](https://link.springer.com/article/10.1007/s42979-024-02970-7)

📌 **Authors:** Mojtaba Jahanian, [Other Authors]

## 🚀 Usage
```python
from clustering_eval.ncqi import normalized_clustering_quality_index
import numpy as np

# Generate random data and labels
X = np.random.rand(100, 10)
labels = np.random.randint(0, 3, size=100)

# Compute NCQI Score
ncqi_score = normalized_clustering_quality_index(X, labels)
print("NCQI Score:", ncqi_score)
```

## 🏆 Features
- **Evaluates clustering quality** using a novel metric based on cohesion and separation.
- **Supports multiple clustering algorithms** including KMeans, Agglomerative Clustering, DBSCAN, and Spectral Clustering.
- **Scalable** for large datasets such as CIFAR-10.
- **Easy integration** into machine learning workflows.

## 📊 Example: Clustering CIFAR-10
```bash
python examples/cifar10_clustering.py
```
This example performs clustering on the CIFAR-10 dataset and evaluates the clustering results using **NCQI**.

## 🔹 Creating and Publishing the Package
### **Step 1: Build the Package**
```bash
python setup.py sdist bdist_wheel
```
✅ This command creates `dist/` and `build/` folders containing the final package files.

### **Step 2: Upload to PyPI**
```bash
twine upload dist/*
```
🔹 Enter your **PyPI username and password** when prompted.

### **Step 3: Install from PyPI**
```bash
pip install clustering_eval
```

## 📜 License
This project is licensed under the MIT License.

📥 **Download the package:** [clustering_eval_package.zip](sandbox:/mnt/data/clustering_eval_package.zip)
