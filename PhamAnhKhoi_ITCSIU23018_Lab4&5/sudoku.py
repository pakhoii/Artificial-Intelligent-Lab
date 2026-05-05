# THE FUNCTION WHICH SOLVES ALL THE SUDOKU PROBLEMS
# IN THE INPUT FILE USING BACKTRACKING AND WRITES THE OUTPUT TO THE OUTPUT FILE

from search import *
import time
import argparse
import os

#THE MAIN FUNCTION GOES HERE
if __name__ == "__main__":
    """
    The function takes arguments from commandline as follow
    python sudoku.py --inputFile data/euler.txt --method AC3
    """
    argument_parser = argparse.ArgumentParser(description="Sudoku Solving Problem")
    argument_parser.add_argument("--inputFile", type=str, help="Sudoku Input File")
    argument_parser.add_argument("--method", type=str, help="The method to solve the problem")
    args = argument_parser.parse_args()

    filename = args.inputFile
    method = args.method if args.method else "Backtracking"
    
    input_basename = os.path.splitext(os.path.basename(filename))[0]
    output_filename = f"output_{method}_{input_basename}.txt"
    
    array = []  
    with open(filename, "r") as ins:
        for line in ins:
            array.append(line)
    ins.close()
    i = 0
    boardno = 0
    start = time.time()
    f = open(output_filename, "w")
    for grid in array:
        startpuzle = time.time()
        boardno = boardno + 1
        sudoku = csp(grid=grid)
        
        if method == "AC3":
            solved = AC3_Search(sudoku)
        else:
            solved = Backtracking_Search(sudoku)
            
        print("The board - ", boardno, " takes ", time.time() - startpuzle, " seconds")
        if solved != "FAILURE":
            print("After solving: ")
            display(solved)
            f.write(write(solved)+"\n")
            i = i + 1

    f.close()
    print ("Number of problems solved is: ", i)
    print ("Time taken to solve the puzzles is: ", time.time() - start)