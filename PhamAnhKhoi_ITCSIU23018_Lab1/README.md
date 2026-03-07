# HOW TO COMPILE AND RUN THIS CODE

> Notice: Make sure that you are at the folder `/PhamAnhKhoi_ITCSIU23018_Lab1`.
> 
> For example: `E:\ForCoding\Artificial-Intelligent-Lab\PhamAnhKhoi_ITCSIU23018_Lab1>`

## Setting Up
Since I use `uv` Python toolchain to manage environments and dependencies. So if your device already has `uv`, please follow the below instructions

1. Download all necessary dependencies
    ```bash
    uv sync # uv will automatically create the virtual environment which the approriate python version for you
    ```

2. Activate the virtual environment
    ```bash
    ./.venv/Scripts/Activate.ps1 # For Windows
    source .venv/bin/activate # For MacOS and Linux
    ```

Otherwise, if `uv` has not been downloaded yet, you can download it via this [link](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer). Or you can choose the traditional approach like

```bash
# Create Python 3.9 virtual environment
python3.9 -m venv .venv

# Activate the virtual environment
# Windows
./.venv/Scripts/Activate.ps1

# MacOS / Linux
source .venv/bin/activate

# Install required packages
pip install ipython numpy
```

## Runing the code
Please type in this command to run the program.
```bash
python run_lab1.py
```