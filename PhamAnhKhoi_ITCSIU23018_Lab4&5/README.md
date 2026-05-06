# HOW TO COMPILE AND RUN THIS CODE

> Notice: Make sure that you are at the folder `/PhamAnhKhoi_ITCSIU23018_Lab4&5/`.
> 
> For example: `E:\ForCoding\Artificial-Intelligent-Lab\PhamAnhKhoi_ITCSIU23018_Lab4&5>`

## Setting Up Environment
The python version is 3.9.x, so you can choose any way to create a virtual environment with python 3.9. In this case, I will use conda.
```bash
conda create -n lab3 python=3.9
```

Then type these command into the terminal
```bash
conda activate lab3
pip install "numpy>=2.0.2" "ipython>=8.18.1"
```

## Run the code
Change directory into `/Lab3`.

To run the code on the Euler Sudoku dataset
```bash
python sudoku.py --inputFile data/euler.txt --method Backtracking # For backtracking method
python sudoku.py --inputFile data/euler.txt --method AC3 # For AC3 method
```

To run the code on the Magic Tour Sudoku dataset
```bash
python sudoku.py --inputFile data/magictour.txt --method Backtracking # For backtracking method
python sudoku.py --inputFile data/magictour.txt --method AC3 # For AC3 method
```
