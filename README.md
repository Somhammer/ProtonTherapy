ProtonTherapy Simulation Tool
-------------
The ProtonTherapy Simulation Tool makes the TOPAS input parameter files with easy modifying parameters value and executes the TOPAS with the parameter file.

### Download

```
git cone https://github.com/Somhammer/ProtonTherapy.git
```

### Requirement:
* matplotlib
* pydicom
* numpy
* pandas
* openpyxl
* xlrd

### Setup:
It writes your directory path in topas parameters files as absolute path. 
Because the relative path makes an error during running the TOPAS, please, run this setup script.

```
./setup.sh
```

This tool is based on python3, therefore, setting up the virtual environment is better.

#### Conda environment
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

#### Installation of required packages

Before installation of required packages, activate conda environment.

```python
conda install matplotlib
conda install -c conda-forge pydicom
conda install numpy
conda install pandas
conda install openpyxl
conda install xlrd
```

### Usage
#### Calculation of dose scaling factor
To fit between the patient and MC data, the scale of dose of MC should be applied.
This package requires the CT, RT, RS, RD and convAlgo files.
* CT: the patients computer tomography image files.
* RT: the radio therapy plan file.
* RS: the radio therapy structure file.
* RD: the radio therapy dose file.
* ConvAlgo(Convenient algorithm): Matching parameters between the plan and treatment machine.
After preparing these files, write the parameters in prod/doseScaling\_cfg.py

```python
# In the cfg file, you should fill the parameter dictionary.
parameters = {
  "virtualSID":230,
  "DoseScalingF":10000,
  "nNodes": 0, # Number of threads
  "nHistory": 2000, # Number of history of MC
  # Relative path from data directory
  "DicomDirectory":"Patient",
  "ConvAlgo":"Patient.xls",
  # Relative path from prod directory
  "Output":datetime.today().strftime('%y%m%d')
}
```

Then, run the python with this script.

```python
python3 doseScaling_cfg.py
```

Update: output of each instance, class explanation, final result and plot.

It returns scaling factor and after finishing the post-process, modified dcm file is made.

#### Customization






