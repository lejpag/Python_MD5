# THe purpose of this code is to solve the skyscrapers game.
# Also know as Towers, see https://www.puzzle-skyscrapers.com/
# The rules are simple.
# The objective is to place skyscrapers in all cells on the grid according to the rules:
#- The height of the skyscrapers is from 1 to the size of the grid i.e. 1 to 4 for a 4x4 puzzle.
#- You cannot have two skyscrapers with the same height on the same row or column.
#- The numbers on the sides of the grid indicate how many skyscrapers would you see if you look in the direction of the arrow.
# Those numbers on the sides will be refered to as "conditions"
# The heights of the skyscrapers will be often refered as "values"

# FAIL FAIL FAIL
# does not work with enpty conditions

import sys

grid_size = input("Hi, please enter the grid size: ")

n = int(grid_size)

debug = 0

# The following function will display the grid, values, and conditions in the console
# This can be done in more elegant manner but I did not know about formatted string at that time

def full_display(S,L,U,R,D):
    u = "   "
    for val in U: 
        if val:
            u = u + str(val) + "   "
        else:
            u = u + " " + "   "
    
    d = "   "
    for val in D:
        if val:
            d = d + str(val) + "   "
        else:
            d = d + " " + "   "
    
    l=[]
    
    for i in range(n):
        if str(L[i]):
            l.append(str(L[i]) + "|")
        else:
            l.append(" " + "|")
        for j in range(n):
            #if the value is not 0
            if S[i][j]:
                l[i] = l[i] + " " + str(S[i][j]) + " |"
            #if value is 0 then do no print anything
            else:
                l[i] = l[i] + " " + " " + " |"
        l[i] = l[i] + str(R[i])
            
    line = " +" + n*"---+"
    
    print(u)
    print(line)
    for i in range(n): print(l[i])
    print(line)
    print(d)

# initial user inputs
# the user can specify the conditions manually or choose some preset values

print("\nPlease now enter the values around the grid\n")    

S = [[" " for i in range(n)] for j in range(n)]
L,R,D,U = [" "]*n,[" "]*n,[" "]*n,[" "]*n

for i in range(4*n):
    if i < n:
        U[i] = "x"
        full_display(S,L,U,R,D)
        ans = input("please enter the value of \"x\" : ")
        U[i] = int(ans) if ans else ""
    if i >= n and i < 2*n:
        R[i%n] = "x"
        full_display(S,L,U,R,D)
        ans = input("please enter the value of \"x\" : ")
        R[i%n] = int(ans) if ans else ""
    if i >= 2*n and i < 3*n:
        D[i%n] = "x"
        full_display(S,L,U,R,D)
        ans = input("please enter the value of \"x\" : ")
        D[i%n] = int(ans) if ans else ""
    if i >= 3*n:
        L[i%n] = "x"
        full_display(S,L,U,R,D)
        ans = input("please enter the value of \"x\" : ")
        L[i%n] = int(ans) if ans else ""
        
full_display(S,L,U,R,D)
       
choice = input("Would you like to add some values inside the grid ? (y/n)")

if choice == "y":
    for i in range(n):
        for j in range(n):
            S[i][j] = "x"
            full_display(S,L,U,R,D)
            ans = input("please enter the value of \"x\" : ")
            S[i][j] = int(ans) if ans else 0
    
    full_display(S,L,U,R,D)                 
      
else:
    S = [[0 for i in range(n)] for j in range(n)]

print("\n--> Thank you, let's solve this !\n")
#grid to be filled
#we decided to initialize the grid with  "0"
#there is no confusion as 0 cannot be a height of building (positive integer)
#it will also ease the logical tests, 0 being considered as False by Python
    



#kill flags matrix
#the below matrix will enable the backtracking algorithm to decide whether
#it consider the value as potentially good or wrong
K = [[0 for i in range(n)] for j in range(n)]

# another flag matrix for values that are known good
# for instance values given at the begining of the game
G = [[0 for i in range(n)] for j in range(n)]


#####################################
# counting functions
#####################################
#cL (count left)  returns the number of towers visible from left side on line i
def cL(S,i):

    hmax = S[i][0]
    if hmax > 0:
        #in this case there is building, so it is visible
        c = 1
    else:
        #no building on first cell so we initialize the counter to 0
        c = 0
    #we then check the line from left to right, comparing each new value
    #to the maximum of the previous values
    j = 1
    while hmax < n and j < n:
        #if the new value is bigger than hmax, it means the building is visible
        if S[i][j] > hmax:
            hmax = S[i][j]
            c = c+1
        j = j+1
        
    return c

#cR (count Right)  returns the number of towers visible from Right side on line i
def cR(S,i): 
    hmax = S[i][n-1]
    
    if hmax > 0:
        c = 1
    else:
        c = 0
        
    j = n-2
    while hmax < n and j >= 0:
        if S[i][j] > hmax:
            hmax = S[i][j]
            c = c+1
        j = j-1
        
    return c

#cU (count Up)  returns the number of towers visible from the top on column j
def cU(S,j):    
    hmax = S[0][j]
    
    if hmax > 0:
        c = 1
    else:
        c = 0
        
    i = 1
    while hmax < n and i < n:
        if S[i][j] > hmax:
            hmax = S[i][j]
            c = c+1
        i = i+1
        
    return c

#cR (count Down)  returns the number of towers visible from the bottom on the column j
def cD(S,j):
    hmax = S[n-1][j]   
    
    if hmax > 0:
        c = 1
    else:
        c = 0
        
    i = n-2
    while hmax < n and i >= 0 :
        if S[i][j] > hmax :
            hmax = S[i][j]
            c = c+1
        i = i-1
        
    return c

###################################
    

# The backtracking algorithm needs to check every proposition to decide whether 
# it should keep it (and go ahead) or not (and try another value/go backward).
# The following function checks whether a single building's height at position i,j
# matches the conditions or not.
 
def check(S,L,U,R,D):
    #we can have just one building of a given height per row
    for row in S:
        for val in range(1,n+1):
            if row.count(val) > 1: return False
    
    #we can have just one building of a given height per column
    for k in range(n):
        for val in range(1,n+1):
            if [row[k] for row in S].count(val) > 1: return False
    
    #check of side conditions, when applicable
    for k in range(n):
        if not 0 in S[k]:
            if cL(S,k)!=L[k] and L[k]: return False
            if cR(S,k)!=R[k] and R[k]: return False
        #the next block is optional, uncomplete lines can be ignored
        else:
            if L[k]:
                if cL(S,k) > L[k]: return False 
#           
# One may think adding the check from ride site  "if cR(S,k) > R[k]: return False"
# is a good idea but no
# it can stop the construction of a valid solution
# example if a line is 4 2 1 3 with condition 1 (left) and 2 (right)
# the algorithm would stop at 4 2 1 0 because at this time we can 3 buildings from the right...
    
    #let's check columns now
    for k in range(n):
        #complete columns must satisfy the conditions
        if not 0 in [row[k] for row in S]:
            if cU(S,k) != U[k] and U[k]: return False
            if cD(S,k) != D[k] and D[k]: return False
        #next block is optional, it is enough to check the complete columns
        else:
        #uncomplete columns need to satisfy at least the upper condition
            if U[k]:
                if cU(S,k) > U[k]: return False
        
    return True
    
#####################################

# The backtracking algorithm requires to be able to go back and forth in the grid
# therefore we will not use a standard "for" loop but a "while" and increment
# or decrement the indexes as we need.
# this is why we need those two sweet functions:

def prev(i,j):
    #returns the position of the element to the left, 
    # except when there is no element on the left
    # ie when we are on the first column
    return [i,j-1] if j > 0 else [i-1,n-1]

def nextt(i,j):
    #returns the position of the element to the right,
    # except when there is no element on the right
    # ie when we are on the last column
    return [i,j+1] if j < n-1 else [i+1,0]
    


#know values for trivial cases
for i in range(n):
    if L[i] == 1: S[i][0] = n
    
    if R[i] == 1: S[i][n-1] = n

    if L[i] == n: S[i] = [val for val in range(1,n+1)]

    if R[i] == n: S[i] = [val for val in range(n,0,-1)]
    
#know values for trivial cases
for j in range(n):
    if U[j] == 1: S[0][j] = n
    
    if D[j] == 1: S[n-1][j] = n
    
    if U[j] == n: 
        for i in range(n):
            val = i+1
            S[i][j] = val
            
    if D[j] == n:
        for i in range(n):
            val = n-i
            S[i][j] = val    

print("Adding possible trivial values found before computation :\n")
full_display(S,L,U,R,D)
    
# good flags matrix generation
for i in range(n):
    for j in range(n):
        if S[i][j]: G[i][j] = 1
        
#####################################
#main loop, let's kill it backtrack style !
        
iteration = 0   
i,j = 0,0
    
while (i,j) < (n,0):
    if debug: print("i,j=",i,j)
    
    #if no value has been set previously (S[i][j]=0) let's begin with a 1
    if not S[i][j] : S[i][j] = 1
    
    if debug: print(check(S,L,U,R,D))
    
    #if this value matches and the cell has not been flagged as killed we go ahead
    if check(S,L,U,R,D) and not K[i][j]:
        i,j = nextt(i,j)
    
    #but if not, it means that we should try another value
    #or go back if there is no other value to try :(
    else:
        if G[i][j]:
            if K[i][j]: K[i][j] = 0
            i,j = prev(i,j)
            K[i][j] = 1
        else:
            if S[i][j] < n:
                #In this case it is possible to try the next value
                S[i][j] = S[i][j] + 1
                #the possible kill flag must be set to 0 to allow the algorithm to proceed
                #if this new value satisfies the conditions
                if K[i][j]: K[i][j] = 0
            else:
                #in this case all possible values have been tried for cell i,j
                #it means that a former value was already wrong
                #we need to go back, so we reinitialize the value to 0
                S[i][j] = 0
                #we remove the possible kill flag
                if K[i][j]: K[i][j] = 0
                #go one step back
                i,j = prev(i,j)
                #flag the former value as killed to force the algoritm to try another value
                K[i][j] = 1
            
    if debug: full_display(S,L,U,R,D)
    
    iteration = iteration + 1



         
print("\n And the solution is...\n")    
full_display(S,L,U,R,D)
print("\n#iteration =",iteration)    
        
        
    