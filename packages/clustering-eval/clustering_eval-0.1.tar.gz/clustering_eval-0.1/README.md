# Clustering Evaluation (NCQI)

A Python package for evaluating clustering algorithms using the **Normalized Clustering Quality Index (NCQI)**.

## 📌 Installation
To install the package, run:
```bash
pip install git+https://github.com/Mojtaba-jahanian/Cosine-Clustering-Index-CCI-.git
```

## 📊 Example: Clustering CIFAR-10
```bash
python examples/cifar10_clustering.py
```

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
