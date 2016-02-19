'''
Implements Hungarian Algorithm to find perfect matching of maximum weight
within a weighted bipartite graph.

See
http://www.math.harvard.edu/archive/20_spring_05/handouts/assignment_overheads.pdf
https://en.wikipedia.org/wiki/Hungarian_algorithm
http://www.wikihow.com/Use-the-Hungarian-Algorithm
http://math.stackexchange.com/questions/590305/finding-the-minimum-number-of-lines-to-cover-all-zeros-in-an-assignment-probem
http://www.cimat.mx/~omar/optimizacion2/assignment.pdf
http://csclab.murraystate.edu/bob.pilgrim/445/munkres.html
'''

def find_max(weight_matrix):
    return max(max(w for w in row) for row in weight_matrix)

def make_square(weight_matrix, height, width, max_entry):
    if height<width: #then add rows
        weight_matrix += [[max_entry]*width]*(width-height)
    if width<height: #then add col.s
        weight_matrix = [row+[max_entry]*(height-width) for row in weight_matrix]
    return weight_matrix, max(height,width), (max(height,width)-min(height,width))*max_entry

def reduce_entries(weight_matrix, height, width):
    for r in range(height):
        row = weight_matrix[r]; min_entry = min(row)
        weight_matrix[r] = [rowj-min_entry for rowj in row]
    transpose = list(zip(*weight_matrix))
    for c in range(width):
        col = transpose[c]; min_entry = min(col)
        transpose[c] = [colj-min_entry for colj in col]
    return [list(t) for t in zip(*transpose)]

def min_num_lines(weight_matrix, side):
    row_assignments = []
    col_assignments = []
    for r,row in enumerate(weight_matrix):
        cs = [c for c in range(side) if row[c]==0 and c not in col_assignments] #find unassigned 0's
        if cs:
            row_assignments.append(r)
            col_assignments.append(cs[0])

    transpose = list(zip(*weight_matrix))
    row_ticks = set(r for r in range(side) if r not in row_assignments)
    col_ticks = set()
    while True:
       sizec = len(col_ticks)
       col_ticks = set(c for c in range(side) if c in col_ticks or \
                                                 min(transpose[c][r] for r in row_ticks)==0)
       row_ticks = set(r for r in range(side) if r in row_ticks or \
                                                 [] != list(0 for rr,cc in zip(row_assignments,col_assignments) if rr==r and cc in col_ticks))
       if sizec==len(col_ticks):
           break

    if side == len(col_ticks) + side-len(row_ticks):
        return 'done', row_assignments, col_assignments

    m = min(weight_matrix[r][c] for r in row_ticks for c in range(side) if c not in col_ticks)
    #print(weight_matrix)
    for r in range(side):
        for c in range(side):
            weight_matrix[r][c] += -m if r in row_ticks and c not in col_ticks else \
                                   +m if r not in row_ticks and c in col_ticks else \
                                    0
    return weight_matrix

def minweight(weight_matrix, height, width):
    max_entry = find_max(weight_matrix)
    weight_matrix, side, overshoot = make_square(weight_matrix, height, width, max_entry)
    original = [row[:] for row in weight_matrix]
    while True:
        weight_matrix = reduce_entries(weight_matrix, side, side)
        print(weight_matrix)
        X = min_num_lines(weight_matrix, side)
        if X[0]=='done':
            return sum(original[r][c] for r,c in zip(X[1],X[2]))-overshoot
        weight_matrix = X

A = [[250,400,350],[400,600,350],[200,400,250]]
print(minweight(A, 3, 3))
#A = [[1,2,3],[40,50,60]]
#print(minweight(A, 2, 3))
