Proton Therapy Simulation Tool
-------------
The ProtonTherapy Simulation Tool makes the TOPAS input parameter files easily

Korean manual: [Korean](https://github.com/Somhammer/ProtonTherapy/blob/main/README_KR.md)

English manual: [English](https://github.com/Somhammer/ProtonTherapy/blob/main/README.md)

### Download

```
git cone https://github.com/Somhammer/ProtonTherapy.git
```

### Installation
#### Python
To run the ProtonTherapy, python is needed. Development and test was done on python 3.9

#### Libraries
ProtonTherapy uses the following libraries.

* pyqt5
* pydicom
* numpy
* matplotlib
* pandas
* openpyxl
* xlwings
* yaml

If you use pip, you can install above libraries easily. Also, you can use pip like this.

```
# Usage : pip install libraries
pip install pyqt5 pydicom numpy matplotlib pandas openpyxl xlwings pyyaml
```

#### Using virtual environment of Anaconda
To manage the version of python and libraries, you can use Anaconda. You can install Anaconda at the following address: (https://www.anaconda.com/products/individual#download-section)
Also, you can refer to the following document for installation: (https://docs.anaconda.com/anaconda/install/index.html)

If your os is Linux, you can install it easily with the following command.

```
bash Anaconda3-2020.11-Linux-x86_64.sh
```

After installation, if Anaconda executes automatically when you open the terminal, write the following command.

```python
conda config --set auto_activate_base false
```

Anaconda's virtual environment is set up by the following.

```python
# Anaconda update
conda update -n base -c defaults conda
# Virtual environment creation command: conda create -n {가상환경 이름} python={Python 버전}
# Please remove the curly braces ({,}) when writing it.
conda create -n py39 python=3.9
# Virtual environment activation
conda activate py39
# Virtual environment deactivation
conda deactivate
```

After the virtual environment is activated, you can install the required packages in the following way.

```python
conda install pyqt5
conda install matplotlib
conda install -c conda-forge pydicom
conda install numpy
conda install pandas
conda install openpyxl
conda install xlrd
conda install pyyaml
```
