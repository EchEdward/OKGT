import numpy as np

An = np.array([[1,0,0,0,0],
                [0,1,0,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,0,0,1]], dtype=np.float64)
Ak = An


Zsourse = np.array([[10**6,0,0,0,0],
                [0,10**6,0,0,0],
                [0,0,10**6,0,0],
                [0,0,0,10**-3,0],
                [0,0,0,0,10**-3]], dtype=np.float64)

Zln = np.zeros((5,5),dtype=np.complex128)

for i in range(5):
    for j in range(5):
        if i==j:
            Zln[i][j] = 1.0 + 1.0j*10**-3
        else:
            Zln[i][j] = 0.9 + 0.9j*10**-3

J1 = np.array([10, 0.001, 0.001, 0, 0], dtype=np.complex128)
J2 = np.array([-5, -0.001, -0.001, 0, 0], dtype=np.complex128)

Yground = np.array([[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,10**6+1/4,-10**6],
                    [0,0,0,-10**6,10**6]], dtype=np.complex128)

Yfault = np.array([[10**6,0,0,-10**6,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [-10**6,0,0,2*10**6+1/4,-10**6],
                    [0,0,0,-10**6,10**6]], dtype=np.complex128)

Yps = np.array([[5*10**6+1/0.5,-10**6,-10**6,-10**6,-10**6],
                    [-10**6,10**6,0,0,0],
                    [-10**6,0,10**6,0,0],
                    [-10**6,0,0,10**6,0],
                    [-10**6,0,0,0,10**6]], dtype=np.complex128)

A = np.zeros((7*5,6*5), dtype=np.float64)

for j in range(0,6*5,5):
    A[j:j+5,j:j+5] = An
    A[j+5:j+10,j:j+5] = Ak

Z = np.zeros((6*5,6*5),dtype=np.complex128)

for i in range(0,6*5,5):
    if i == 0 or i == 6*5-5:
        Z[i:i+5,i:i+5] = Zsourse
    else:
        Z[i:i+5,i:i+5] = Zln

Ydop = np.zeros((7*5,7*5),dtype=np.complex128)
J = np.zeros((7*5,),dtype=np.complex128)
for i in range(0,7*5,5):
    if i == 0:
        1
        Ydop[i:i+5,i:i+5] = Yps
        J[i:i+5] = -J1
        J[i+5:i+10] = J1
    elif i == 6*5:
        1
        Ydop[i:i+5,i:i+5] = Yps
        J[i-5:i] = J2
        J[i:i+5] = -J2
    elif i == 3*5:
        1
        Ydop[i:i+5,i:i+5] = Yfault
    else:
        1
        Ydop[i:i+5,i:i+5] = Yground

dZ = np.diag(Z.diagonal())
W = Z - dZ
dY = np.linalg.inv(dZ)

Ymain = np.dot(np.dot(A,dY), A.transpose())
Ymain += Ydop

JE = np.hstack([J,np.zeros((6*5,),dtype=np.complex128)])

KI = np.dot(A, np.dot(W, dY.transpose()))

YZ = np.vstack([np.hstack([Ymain,KI]),np.hstack([A.transpose(),Z])])

Rez = np.linalg.solve(YZ, JE)

for i in range(7*5,7*5+6*5):
    print(np.abs(Rez[i]))

i = 10
a = f"xaxaxaxa_{i}"
print(a)