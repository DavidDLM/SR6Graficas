# Operaciones con matrices obtenidas de varias fuentes
import math


# https://stackoverflow.com/questions/40120892/creating-a-matrix-in-python-without-numpy
def createMatrix(rowCount, colCount, dataList):
    mat = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            # you need to increment through dataList here, like this:
            rowList.append(dataList[rowCount * i + j])
        mat.append(rowList)

    return mat


# https://stackoverflow.com/questions/28253102/python-3-multiply-a-vector-by-a-matrix-without-numpy
def multMatrix(v, G):
    result = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    for i in range(len(v)):  # this loops through columns of the matrix
        total = 0
        # this loops through vector coordinates & rows of matrix
        for j in range(len((G[0]))):
            for k in range(len(G)):
                result[i][j] += v[i][k] * G[k][j]
    return result


# Function to print identity matrix
# https://www.geeksforgeeks.org/python-program-for-identity-matrix/
def identityMatrix(size):
    matrix = []
    for row in range(0, size):
        matrix.append([])
        for col in range(0, size):
            # Here end is used to stay in same line. Append instead of print
            if (row == col):
                matrix[row].append(1)
                #print("1 ", end=" ")
            else:
                matrix[row].append(0)
                #print("0 ", end=" ")
    return matrix


# https://stackoverflow.com/questions/35208160/dot-product-in-python-without-numpy
def dotMatrix(v1, v2):
    return sum([x*y for x, y in zip(v1, v2)])


# Simplemente multiplicar vectores
def vectMultMatrix(M, v):
    return [dotMatrix(r, v) for r in M]


# https://www.statology.org/cross-product-python/
def crossProductMatrix(A, B):
    result = [A[1]*B[2] - A[2]*B[1],
              A[2]*B[0] - A[0]*B[2],
              A[0]*B[1] - A[1]*B[0]]
    return result


# Transpose matrix
def transposeMatrix(m):
    return map(list, zip(*m))


# Tres funciones para poder hallar el determinante de una matriz sin numpy
# https://integratedmlai.com/find-the-determinant-of-a-matrix-with-pure-python-without-numpy-or-scipy/
def zerosMatrix(rows, cols):
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)
    return M


def copyMatrix(M):
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])

    # Section 2: Create a new matrix of zeros
    MC = zerosMatrix(rows, cols)

    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC


def determinantMatrix(m):
    # base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c] * \
            determinantMatrix(getMatrixMinor(m, 0, c))
    return determinant


# Substract
def subtractVectors(v1, v2):
    result = [i-j for i, j in zip(v1, v2)]
    return result


# Eliminate
def eliminateMatrix(r1, r2, col, target=0):
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]


# Norm fuction
def normMatrix(list):
    dist = math.sqrt(((list[0] - list[1]) ** 2)
                     + ((list[1] - list[2]) ** 2)
                     + ((list[2] - list[0]) ** 2))

    return dist


# Magnitud
def magnitudeMatrix(m):
    b = 0
    a = 0
    for i in m:
        a = i**2
        b += a
    b = b**0.5
    return b


# Matrix inversion dos funciones
# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
def getMatrixMinor(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                raise ValueError("Matrix is not invertible")
        for j in range(i+1, len(a)):
            eliminateMatrix(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminateMatrix(a[i], a[j], i)
    for i in range(len(a)):
        eliminateMatrix(a[i], a[i], i, target=1)
    return a


def inverseMatrix(a):
    tmp = [[] for _ in a]
    for i, row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    getMatrixMinor(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i])//2:])
    return ret
