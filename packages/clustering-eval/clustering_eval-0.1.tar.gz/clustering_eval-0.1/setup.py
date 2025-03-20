from setuptools import setup, find_packages

# خواندن توضیحات از README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clustering_eval",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "tensorflow",
        "matplotlib",
        "pandas"
    ],
    author="Mojtaba Jahanian",
    author_email="mojtaba160672000@aut.ac.ir",
    description="A package for evaluating clustering algorithms using NCQI.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # تنظیم نوع متن برای Markdown
    url="https://github.com/Mojtaba-jahanian/Cosine-Clustering-Index-CCI-",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


setup(
    name="clustering_eval",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "tensorflow",
        "matplotlib",
        "pandas"
    ],
    author="Mojtaba Jahanian",
    author_email="your_email@example.com",
    description="A package for evaluating clustering algorithms using NCQI.",
    url="https://github.com/Mojtaba-jahanian/Cosine-Clustering-Index-CCI-",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
