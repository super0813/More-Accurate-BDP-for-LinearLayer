from gurobipy import *
from Constants import *
import operator
from functools import reduce
import time
import math

filename_result = 'result.txt'
file_name = "demo.lp"
f = open(file_name, 'w')
file2_name = ['Paarshrunkmatrix.txt', 'Paarshrunkmatrix2.txt','BPshrunkmatrix.txt','BPshrunkmatrix2.txt','BPshrunkmatrix3.txt','BPshrunkmatrix4.txt']
file3_name = ['PaarInAES.txt', 'XZInAES.txt', 'XZInAES2.txt']


def get_new_var():
    global count
    var = 'u' + str(count)
    count += 1
    return var


def ObjectiveFunction(f, Rounds):
    for j in range(127):
        f.write("a_" + str(Rounds) + "_" + str(j) + " + ")
    f.write("a_" + str(Rounds) + "_" + str(127) + "\n")


def ShuffleCell(f, Rounds):
    for i in range(Rounds, Rounds + 1):
        for j in range(16):
            for k in range(8):
                f.write("x_%d_%d - b_%d_%d = 0\n" % (i, 8 * j + k, i, P[j] * 8 + k))


def firstCol(f, Rounds):
    for i in range(3):
        for j in range(8):
            f.write("sx_" + str(0) + "_" + str(P[i] * 8 + j) + " - " + "x_" + str(0) + "_" + str(
                i * 8 + j) + " = 0\n")
    for i in range(23):
        f.write("x_%d_%d + " % (0, i))
    f.write("x_%d_%d" % (0, 23))
    for i in range(32):
        f.write(" - y_%d_%d" % (0, i))
    f.write(" = 0\n")


def Permutation(f, Rounds):
    for i in range(Rounds, Rounds + 1):
        for j in range(128):
            f.write("a_" + str(i + 1) + "_" + str(j) + " - " + "y_" + str(i) + "_" + str(j) + " = 0\n")

def Permutation2(f, Rounds):
    for i in range(32, 128):
        f.write('x_0_%d' %i + ' - y_0_%d = 0\n' %i)


def ConstraintBySbox(f, Rounds):
    # temp = []
    for i in range(Rounds, Rounds + 1):
        for j in range(16):
            # temp = []
            for coff in S_T:
                temp = []
                for k in range(8):
                    a = str(coff[k]) + " a_" + str(i) + "_" + str(8 * j + k) + " + "
                    temp.append(a)
                for k in range(7):
                    b = str(coff[k + 8]) + " b_" + str(i) + "_" + str(8 * j + k) + " + "
                    temp.append(b)
                c = str(coff[15]) + " b_" + str(i) + "_" + str(8 * j + 7)
                temp.append(c)
                temp1 = ''.join(temp)
                temp1 = temp1.replace("+ -", "- ")
                s = str(-coff[NUMBER - 1])
                s = s.replace("--", "")
                temp1 += " >= " + s
                f.write(temp1)
                f.write("\n")


def gengerate_list(num):
    listA = []
    for i in range(1):
        with open(file2_name[num])as f:
            line = f.readline()
            while line:
                line = line.replace('+', '').replace('=', '').split()
                listB = []
                for item in line:
                    if item[0] == 't':
                        listB.append(item[0] + str(int(item[1:]) + (200 * i)))
                    else:
                        listB.append(item[0] + str(int(item[1:]) + (32 * i)))
                listA.append(listB)
                line = f.readline()
    return listA


def gengerate_list2(num):
    listA = []
    for i in range(4):
        with open(file3_name[num])as f:
            line = f.readline()
            while line:
                line = line.replace('+', '').replace('=', '').split()
                listB = []
                for item in line:
                    if item[0] == 't':
                        listB.append(item[0] + str(int(item[1:]) + (200 * i)))
                    else:
                        listB.append(item[0] + str(int(item[1:]) + (32 * i)))
                listA.append(listB)
                line = f.readline()
    return listA


def matrix(f, Rounds, num2):
    if Rounds == 0:
        listB = gengerate_list(num2)
    else:
        listB = gengerate_list2(num2)
    listC = listB.copy()
    for item1 in listB:
        listD = []
        listC.remove(item1)
        if len(listC) > 0:
            listE = reduce(operator.add, listC)
        else:
            listE = []
        for i in range(1, 3):
            a = int(item1[i][1:])

            if item1[i] in listE:
                v0 = get_new_var()
                v1 = get_new_var()
                if item1[i][0] == 'x':
                    if len(listX[a]) == 0:
                        listX[a].append(item1[i])
                        listX[a].append(v0)
                        listX[a].append(v1)
                        f.write(listX[a][0][0] + '_' + str(Rounds) + '_' + listX[a][0][1:] + ' - ' + listX[a][1][
                            0] + '_' + str(Rounds) + '_' + listX[a][1][1:]
                                + ' - ' + listX[a][2][0] + '_' + str(Rounds) + '_' + listX[a][2][1:] + ' = 0\n')
                        listD.append(listX[a][1])
                        listX[a].remove(listX[a][1])
                    else:
                        listX[a].append(v0)
                        listX[a].append(v1)
                        f.write(listX[a][1][0] + '_' + str(Rounds) + '_' + listX[a][1][1:] + ' - ' + listX[a][2][
                            0] + '_' + str(Rounds) + '_' + listX[a][2][1:]
                                + ' - ' + listX[a][3][0] + '_' + str(Rounds) + '_' + listX[a][3][1:] + ' = 0\n')
                        listD.append(listX[a][2])
                        listX[a].remove(listX[a][1])
                        listX[a].remove(listX[a][1])
                elif item1[i][0] == 'y':
                    listY[a].append(v0)
                    listY[a].append(v1)
                    f.write(
                        listY[a][1][0] + '_' + str(Rounds) + '_' + listY[a][1][1:] + ' - ' + listY[a][2][0] + '_' + str(
                            Rounds) + '_' + listY[a][2][1:] + ' - '
                        + listY[a][3][0] + '_' + str(Rounds) + '_' + listY[a][3][1:] + ' = 0\n')
                    listD.append(listY[a][2])
                    listY[a].remove(listY[a][1])
                    listY[a].remove(listY[a][1])
                else:
                    listT[a].append(v0)
                    listT[a].append(v1)
                    f.write(
                        listT[a][1][0] + '_' + str(Rounds) + '_' + listT[a][1][1:] + ' - ' + listT[a][2][0] + '_' + str(
                            Rounds) + '_' + listT[a][2][1:] + ' - '
                        + listT[a][3][0] + '_' + str(Rounds) + '_' + listT[a][3][1:] + ' = 0\n')
                    listD.append(listT[a][2])
                    listT[a].remove(listT[a][1])
                    listT[a].remove(listT[a][1])


            else:
                if item1[i][0] == 'x':
                    if len(listX[a]) == 0:
                        listX[a].append(item1[i])
                        listD.append(listX[a][0])
                    else:
                        listD.append(listX[a][1])
                        listX[a].remove(listX[a][1])
                elif item1[i][0] == 't':
                    listD.append(listT[a][1])
                    listT[a].remove(listT[a][1])
                else:
                    listD.append(listY[a][1])
                    listY[a].remove(listY[a][1])

        for i in range(1):
            a = int(item1[i][1:])
            if item1[i][0] == 'y':
                if item1[i] in listE:
                    v0 = get_new_var()
                    v1 = get_new_var()
                    listY[a].append(item1[i])
                    listY[a].append(v0)
                    listY[a].append(v1)
                    f.write(
                        listY[a][1][0] + '_' + str(Rounds) + '_' + listY[a][1][1:] + ' - ' + listY[a][0][0] + '_' + str(
                            Rounds) + '_' + listY[a][0][1:] + ' - '
                        + listY[a][2][0] + '_' + str(Rounds) + '_' + listY[a][2][1:] + ' = 0\n')
                    listD.append(listY[a][1])
                    listY[a].remove(listY[a][1])
                else:
                    listY[a].append(item1[i])
                    listD.append(item1[i])
            else:
                if item1[i] in listE:
                    v0 = get_new_var()
                    listT[a].append(item1[i])
                    listT[a].append(v0)
                    listD.append(listT[a][1])
                else:
                    v0 = get_new_var()
                    listT[a].append(item1[i])
                    listT[a].append(v0)
                    listD.append(listT[a][1])
                    listT[a].remove(listT[a][1])
        f.write(listD[0][0] + '_' + str(Rounds) + '_' + listD[0][1:] + ' + ' + listD[1][0] + '_' + str(Rounds) + '_' +
                listD[1][1:] + ' - ' +
                listD[2][0] + '_' + str(Rounds) + '_' + listD[2][1:] + ' = 0\n')


def init(f, Rounds):
    for i in range(3):
        for j in range(8):
            f.write("sx_" + str(0) + "_" + str(P[i] * 8 + j) + " = 1\n")
    for i in range(32, 128):
        f.write("x_" + str(0) + "_" + str(i) + " = 1\n")



def VariableBinary(f, Rounds):
    for i in range(1):
        for j in range(0, 24):
            f.write("x_" + str(i) + "_" + str(j) + "\n")
        for j in range(32, 128):
            f.write("x_" + str(i) + "_" + str(j) + "\n")
        for j in range(128):
            f.write("y_" + str(i) + "_" + str(j) + "\n")

    for i in range(1, Rounds):
        for j in range(128):
            f.write("x_" + str(i) + "_" + str(j) + "\n")
            f.write("y_" + str(i) + "_" + str(j) + "\n")
            f.write("a_" + str(i) + "_" + str(j) + "\n")
            f.write("b_" + str(i) + "_" + str(j) + "\n")
        for j in range(3996):
            f.write("u_" + str(i) + "_" + str(j) + "\n")
    for i in range(Rounds, Rounds + 1):
        for j in range(128):
            f.write("a_" + str(i) + "_" + str(j) + "\n")
    for i in range(3):
        for j in range(8):
            f.write("sx_" + str(0) + "_" + str(P[i] * 8 + j) + "\n")
    for i in range(1615):
        f.write("u_" + str(0) + "_" + str(i) + "\n")


def WriteObjective(f, obj):
    """
    Write the objective value into filename_result.
    """
    f = open(filename_result, "a")
    f.write("The objective value = %d\n" % (round(obj.getValue())))
    eqn1 = []
    eqn2 = []
    for i in range(0, 128):
        u = obj.getVar(i)
        if u.getAttr("x") != 0:
            eqn1.append(u.getAttr('VarName'))
            eqn2.append(round(u.getAttr('x')))
    length = len(eqn1)
    for i in range(0, length):
        s = eqn1[i] + "=" + str(eqn2[i])
        f.write(s)
        f.write("\n")
    f.close()


def SolveModel(f, Rounds):
    time_start = time.time()
    counter = 0
    set = []
    while counter < 128:
        m.optimize()
        obj = m.getObjective()
        if m.Status == 2:
            if obj.getValue() > 1:
                print("Integral Distinguisher Found!\n")
                break
            else:
                f = open(filename_result, "a")
                f.write("************************************COUNTER = %d\n" % counter)
                f.close()
                WriteObjective(f, obj)
                for i in range(128):
                    var = obj.getVar(i)
                    val = round(var.getAttr('x'))
                    if val == 1:
                        set.append(var.getAttr('VarName'))
                        var.ub = 0
                        m.update()
                        counter += 1
                        if counter == 128:
                            print("Integral Distinguisher do NOT exist\n")
                        break
        elif m.Status == 3:
            print("Integral Distinguisher Found!\n")
            break
        else:
            print("Unknown error!")

    f = open(filename_result, "a")
    f.write(str(R) + ' rounds\n')
    f.write("Those are the coordinates set to zero: \n")
    for item2 in set:
        f.write(str(item2))
        f.write("\n")
    f.write("\n")
    time_end = time.time()
    f.write(("Time used = " + str(time_end - time_start)) + '\n')
    f.write('\n')
    f.close()


if __name__ == "__main__":
    R = 4
    f.write("Minimize\n")
    ObjectiveFunction(f, R)
    f.write("Subject to\n")
    init(f, R)
    for i in range(R):
        count = 0
        if i == 0:
            firstCol(f, i)
            for j in range(6):
                listX = [[0 for u in range(0)] for v in range(128)]
                listY = [[0 for u in range(0)] for v in range(128)]
                listT = [[0 for u in range(0)] for v in range(1000)]
                f = open(file_name, 'a')
                matrix(f, i, j)
        else:
            ConstraintBySbox(f, i)
            ShuffleCell(f, i)
            f.close()
            for j in range(3):
                listX = [[0 for u in range(0)] for v in range(128)]
                listY = [[0 for u in range(0)] for v in range(128)]
                listT = [[0 for u in range(0)] for v in range(1000)]
                f = open(file_name, 'a')
                matrix(f, i, j)
        if i == 0:
            Permutation2(f, i)
        Permutation(f, i)
    f = open(file_name, 'a')
    f.write("Binary\n")
    VariableBinary(f, R)
    f.write("End\n")
    f.close()
    m = read("demo.lp")
    SolveModel(f, R)
    m.write("output.sol")