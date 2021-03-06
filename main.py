from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import collections
import numpy as np
import requests
import uvicorn 

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Puzzle(BaseModel): 
    values: list


# get an unsolved puzzle 
@app.get('/puzzle')
def get_UnsolvedPuzzle(): 
    results = puzzle1
    # results = puzzle1sol
    # results = puzzle1sol1
    return results
@app.get('/puzzle2')
def get_UnsolvedPuzzle(): 
    results = puzzle2
    return results
@app.get('/puzzle3')
def get_UnsolvedPuzzle(): 
    results = puzzle3
    return results


# post and verifies a possible solution 
@app.post('/puzzle')
def post_solution(puzzle: Puzzle): 
    verify = verifyPuzzle(puzzle.values) 
    if verify: 
        return True
    return False


# split the puzzle up into rows
def splitRows(puzzle): 
    rows = [] 
    newPuzzle = puzzle.copy()
    for _ in newPuzzle: 
        newRow = []
        for _ in range(0,9): 
            value = newPuzzle.pop(0)
            newRow.append(value)
        rows.append(newRow)
    return rows

# split the puzzle up into columns
def splitColumns(puzzle):
    cols = [[],[],[],[],[],[],[],[],[]] 
    newPuzzle = puzzle.copy()
    idx = 0
    for _ in range(len(puzzle)): # for each value 
        value = newPuzzle.pop(0)
        cols[idx].append(value) 
        idx += 1 
        if idx == 9: 
            idx = 0
    return cols

# split array into the correct 1x9 squares
# split up into sections of three 
def splitRegion(inputArray): 
    regions = np.array(inputArray).reshape((3,3,3,3)).transpose((0,2,1,3)).reshape((9,9)); # uses numpy built in procedures to make a matrix of 3x3
    return regions

# verifys sections of the puzzle 
def verify(inputArray): 
    correctArray = [1, 2, 3, 4, 5, 6, 7, 8, 9] # correct values to check against
    checkArray = inputArray.copy()
    for row in checkArray: 
        if collections.Counter(row) == collections.Counter(correctArray): # if the arrays have the same values
            continue # keep checking all rows 
        return False # break out if values are not valid
    return True

# verify the entire puzzle
def verifyPuzzle(puzzle): 
    # call split rows, columns and region 
    rows = splitRows(puzzle)
    rowsSoln = verify(rows)
    columns = splitColumns(puzzle)
    colSoln = verify(columns)
    regions = splitRegion(puzzle)
    regSoln = verify(regions)

    if rowsSoln and colSoln and regSoln: 
        print("This is a valid solution") 
        return True 
    print("This is an invalid solution")
    return False

puzzle1 = [ 
    "",1,9,4,2,7,8,5,6,
    7,8,6,9,1,5,2,3,4,
    4,5,2,6,8,3,7,1,9,
    9,7,4,1,3,2,5,6,8,
    2,6,1,5,9,8,4,7,3,
    8,3,5,7,6,4,9,2,1,
    5,4,3,8,7,1,6,9,2,
    6,2,7,3,4,9,1,8,5,
    1,9,8,2,5,6,3,4,7
]

puzzle2= [ 
    "", "", "", 1, "", "", 4, 7,  "", 
    "",  "", 2, "",  "", 6,  "",  "", 1,
    1, "",  "", 5, "",  "", 6,  "", 8,
    6,  "", 5,  "",  "",  "", 1, 2,  "", 
    7,  "",  "",  "", 2, 1,  "",  "", 9,
    2,  "",  "", 3, 8, 5,  "",  "",  "", 
    "",  "", 6, "", 5, "", 8, 1,  "", 
    "",  "",  "",  "",  "",  "",  "",  "", 4,
    "",  "", 3, 9, "",  "",  "", 6,  "", 
]
puzzle3 = [
    "", 5, 2, "", "", 3, "", "",  "", 
    4, 6,  "", 9, "",  "",  "",  "", 2,
    7, "",  "",  "",  "", 5, "",  "",  "", 
    "", 3, "",  "", 6, "",  "",  "",  "", 
    "",  "", 8,4, "", 2,7, "",  "", 
    "",  "",  "",  "", 5, "",  "", 3, "", 
    "",  "",  "", 5, "",  "",  "",  "", 3, 
    5, "",  "",  "",  "", 6, "", 1,9,
    "",  "",  "", 1, "",  "", 6,7, "", 
]

# Only used for code testing purposes
# puzzle1sol = [ 
#     3,1,9,4,2,7,8,5,6,
#     7,8,6,9,1,5,2,3,4,
#     4,5,2,6,8,3,7,1,9,
#     9,7,4,1,3,2,5,6,8,
#     2,6,1,5,9,8,4,7,3,
#     8,3,5,7,6,4,9,2,1,
#     5,4,3,8,7,1,6,9,2,
#     6,2,7,3,4,9,1,8,5,
#     1,9,8,2,5,6,3,4,7
# ]

if __name__ == "__main__": 
    uvicorn.run(app, host = "127.0.0.1", port=5000, log_level="info")
