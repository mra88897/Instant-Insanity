import math as math
from itertools import combinations 
import time

obstacles=[]


def colorCheck(colorCount, puzzle,i,j):
    colorCount[puzzle[i][j][0]]+=1
    colorCount[puzzle[i][j][1]]+=1
    
    for w in range(len(colorCount)):
        if(colorCount[w] >= 3):
            colorCount[puzzle[i][j][0]]-=1
            colorCount[puzzle[i][j][1]]-=1
            return False  
    return True

    
def clearColor(colorCount):
    for w in range(len(colorCount)):
        colorCount[w] = 0

        
def isSafe(puzzle,solution, colorCount, i, j):
    #check for array bounds, color collisions , used pairs
    if i < len(puzzle) and j < len(puzzle[0]) and solution[i][j]==0 and colorCheck(colorCount,puzzle,i,j) :
        return True
    return False
  

'''This method checks for a half solution starting from position [i,j]''' 
def solveUtil(puzzle, solNum, solution, colorCount, i, j):
    #reached last row therefore might have a half solution 
    if(i==len(puzzle)-1 and isSafe(puzzle,solution,colorCount,i,j)):
        solution[i][j]=solNum
        return True
    
    if(isSafe(puzzle,solution,colorCount,i,j)):
        #mark node as part of solution 
        solution[i][j]=solNum
        
        #check paths to children 
        if(solveUtil(puzzle,solNum,solution,colorCount,i+1,0)):
            return True
        if(solveUtil(puzzle,solNum,solution,colorCount,i+1,1)):
            return True
        if(solveUtil(puzzle,solNum,solution,colorCount,i+1,2)):
            return True          
        
        #no path to any of the children so unmark node and go back to previous call
        unMarkFromSolution(puzzle,solution,colorCount,i,j)
        return False
        
    return False 

  
def unMarkFromSolution(puzzle,solution,colorCount,i,j):
    solution[i][j]=0
    colorCount[puzzle[i][j][0]]-= 1
    colorCount[puzzle[i][j][1]]-= 1
    
def clearRowsBelow(puzzle,solution,solNum,colorCount,i):
    for s in range(i+1,len(puzzle)):
        for t in range(len(puzzle[0])):
            if(solution[s][t]==solNum): 
                solution[s][t] = 0
                colorCount[puzzle[s][t][0]]-= 1
                colorCount[puzzle[s][t][1]]-= 1
    
    
#returns the column number if a row has a solNum set, otherwise returns -1
def findRowSet(solution, solNum,row):
    for x in range(3):
        if(solution[row][x] == solNum):
            return x
    return -1

    
#returns the most recent row backtracked from if successful, otherwise returns -1 
# i is the initial recentRowIndex
def doBackTrack(puzzle, solNum , solution, colorCount, i):
    while(i>0):
        j = findRowSet(solution,solNum,i)
        
        if(j==-1):
            print(i)
            print("ERROR")   

        tempi = i
        tempj = j
        
        #check the first 2 colums of rows below me; find the position to start dfs again  
        for s in range(i+1,len(puzzle)):
           for t in range(len(puzzle[0]) - 1):
               if(solution[s][t]==solNum and s > tempi): #find the bottom most that is set from rows below me 
                   tempi = s
                   tempj = t
        
        #apply the changes 
        if(tempi!=i):
            i = tempi
            j = tempj 
        
        if(j==0 or j==1):
            #there's stuff we can backtrack
            while(j<2):
                if(solution[i][j]==solNum):
                    unMarkFromSolution(puzzle,solution,colorCount,i,j)
                
                clearRowsBelow(puzzle,solution,solNum,colorCount,i)
                
                j+=1
                
                halfSolutionFound = solveUtil(puzzle, solNum , solution, colorCount, i , j)
                
                if(not halfSolutionFound):
                    #No half sol found. Unmark all the rows below
                    clearRowsBelow(puzzle,solution,solNum,colorCount,i)
                
                if(halfSolutionFound):
                    return i
             
            #nothing works in this row, clear the row and try row above
            for z in range(3):
                if(solution[i][z]==solNum): 
                    solution[i][z]=0
                    colorCount[puzzle[i][z][0]]-= 1
                    colorCount[puzzle[i][z][1]]-= 1
            i-=1
                
        else:
            #nothing to backtrack in this row, clear the row and everything below it and try row above
            clearRowsBelow(puzzle,solution,solNum,colorCount,i-1)

            i-=1
    
    #no half solution found 
    return -1
     
      
'''This method checks for full solutions involving opp pair A and B'''    
def solve(puzzle, pairA, pairB):
    row = len(puzzle)
    col = len(puzzle[0])
    colorCount = [0 for w in range(30 + 1)] #index 0 is unused, initialize all to 0
    colorCount2 = [0 for w in range(30 + 1)]
    solution = [[0]*col for x in range(row)] #create a 2d array with dimensions row x col, initialze all to 0
    
    foundFirstHalfSol = False
    foundSecondHalfSol = False
    backTrack = False
    recentRowIndex = row - 1
    
    while(True):
        #Try to find the first half solution via backtracking or in the first try 
        if(backTrack):
            #clear the secondHalfSol attempt
            for z in range(3):
                for y in range(row):
                    if(solution[y][z]==2):
                        solution[y][z]=0
            
            recentRowIndex = doBackTrack(puzzle, 1, solution ,colorCount, recentRowIndex)
            
            if(recentRowIndex == -1):
                foundFirstHalfSol = False
            else:
                foundFirstHalfSol = True 
        else:
            foundFirstHalfSol = solveUtil(puzzle,1,solution,colorCount,0,pairA)
        
        
        #If first solution found then try finding second one, else no solution 
        if(foundFirstHalfSol):
            clearColor(colorCount2)
            
            foundSecondHalfSol = solveUtil(puzzle,2,solution,colorCount2,0,pairB)
            if(foundSecondHalfSol):
                return True
            else:
                backTrack = True 
        else:
            #First halfSolution never found so no full solution exists using pairA and pairB
            return False 
                
    
#This method checks for an obstacle (subset of cubes with no solution) given an array of puzzles of same size
def obstacleExists(puzzle): 
    for combo in puzzle:
        #find full solution using opp pair 0 and 1
        if (solve(combo, 0, 1)):
            #continue means go to next puzzle (i.e. back to for loop begin)
            continue 
        
        #find full solution using opp pair 1 and 2
        if (solve(combo, 1, 2)):
            continue 

        #find full solution using opp pair 0 and 2
        if (solve(combo, 0, 2)):
            continue 
        
        #none of the pairs work for this subset, then this subset is an obstacle
        print("None of the pairs work")
        print("\nFound an obstacle of size ", len(combo))
        obstacles.append(combo)
        
        #print the obstacle
        for item in combo:
            print(item, " \n")
        return True 
    
    #no obstacles found, therefore all subsets of size n have a solution
    print("All subsets size ", len(combo) ," have a solution")
    return False
        
        
'''This method finds the minimum obstacle of a puzzle'''
def findMinObstacle(origPuzzle):
    #size of minObs 
    minObs = len(origPuzzle) + 1

    for k in range(len(origPuzzle),1, -1): #countdown from length to 2
        comb = combinations(origPuzzle, k) #from origPuzzle choose k
        if(obstacleExists(comb)):
            minObs-=1
        else:
            #solution found for all subsets of puzzlesize k  
            print("\nMinimal obstacle size is ", minObs)
            
            #print min obstacle
            for item in obstacles[len(obstacles)-1]:
                print(item, " \n")
            return 
    
    #all subsets have obstacles therefore min obstacle is size 2
    print("\nMinimal obstacle size is 2")

    
def getPuzzle(pattern):
    puzzle = []
    cube = []
    pair = []
    for i in range(180):
        pair.append(pattern[i])
        if (i + 1) % 2 == 0:
            cube.append(pair)
            pair = [] #reset for next
        if (i + 1) % 6 == 0:
            puzzle.append(cube)
            cube = [] #reset for next
    return puzzle   
  
pattern1 = [(1 + math.floor(i * math.pi) % 30) for i in range(1, 181)]
pattern2 = [(1 + math.floor( i * math.e % 30)) for i in range(1,181)]
pattern3 = [(1 + math.floor( i * math.sqrt(3) ) % 30) for i in range(1,181)]
pattern4 = [(1 + math.floor( i * math.sqrt(5)) % 30) for i in range(1,181)]    

start = time.time()


# Get all the puzzles 
puzzle1 = getPuzzle(pattern1)
#puzzle2 = getPuzzle(pattern2)
#puzzle3 = getPuzzle(pattern3)
#puzzle4 = getPuzzle(pattern4)


test =[[[6,4],[8,12],[2,8]],
      [[4,2],[2,2],[8,2]],
      [[3,5],[3,9],[1,5]],
      [[4,12],[4,10],[4,8]],
      [[7,11],[3,9],[5,7]],
      [[10,12],[6,12],[6,4]],
      [[3,9],[7,11],[11,3]],
      [[12,6],[10,12],[8,8]],
      [[9,11],[1,11],[1,11]],
      [[12,10],[10,6],[4,10]],
      [[9,5],[1,9],[5,9]],
      [[9,11],[1,4],[7,7]]]  


# Driver Code        
findMinObstacle(puzzle1)

end = time.time()
print("Program ran for " , end - start, " seconds")



             
  