ProtonTherapy Simulation Tool
-------------
The ProtonTherapy Simulation Tool makes the TOPAS input parameter files with easy modifying parameters value and executes the TOPAS with the parameter file.

# Download

```
git cone https://github.com/Somhammer/ProtonTherapy.git
```

# Requirement:
* matplotlib
* pydicom
* numpy
* pandas
* openpyxl
* xlrd

# Setup:
It writes your directory path in topas parameters files as absolute path. 
Because the relative path makes an error during running the TOPAS, please, run this setup script.

```
./setup.sh
```

This tool is based on python3, therefore, setting up the virtual environment is better.

## Conda environment
1. Download anaconda installation file in [Anaconda](https://www.anaconda.com/products/individual#download-section)
2. Open the installation file.

```
bash Anaconda3-2020.11-Linux-x86_64.sh
```

3. Install conda following the message in the terminal
4. Initialize conda. If you type 'yes' after installation, conda is initialized automaticcaly. If not, follow the message in the terminal.
5. Conda base is activated automattically after the installation. You can deactivate this by following command.

```python
conda config --set auto_activate_base false
```

6. Create and activate the virtual environment

```python
conda update -n base -c defaults conda # update conda
#conda create -n {name} python={version}
conda create -n py39 python=3.9 # make conda environment
conda activate py39 # activate conda
conda deactivate # deactivate conda
```

## Installation of required packages

Before installation of required packages, activate conda environment.

```python
conda install matplotlib
conda install -c conda-forge pydicom
conda install numpy
conda install pandas
conda install openpyxl
conda install xlrd
```



