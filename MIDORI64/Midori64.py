from gurobipy import *
import operator
from functools import reduce
import time

filename_result = "result.txt"
file_name = "demo.lp"
f = open(file_name, "w")
Constr = []

S_T = [[1, 1, 4, 1, -2, -2, -2, -2, 1],
       [0, 0, -3, 0, 1, 1, -2, 1, 2],
       [0, 0, 0, 0, -1, -1, 2, -1, 1],
       [-1, -1, 0, -1, 2, 2, 2, 2, 0],
       [0, -1, 0, -1, 0, 1, 1, 1, 1]]

P = [0, 10, 5, 15, 14, 4, 11, 1, 9, 3, 12, 6, 7, 13, 2, 8]
state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
NUMBER = 9


def get_new_var():
    global count
    var = "u" + str(count)
    count += 1
    return var


def ObjectiveFunction(f, Rounds):
    eqn = []
    for j in range(64):
        eqn.append("a" + "_" + str(Rounds) + "_" + str(j))
    temp = " + ".join(eqn)
    f.write(temp)
    f.write("\n")


def ShuffleCell(f, Rounds):
    for i in range(Rounds, Rounds + 1):
        for j in range(16):
            for k in range(4):
                temp = "x_%d_%d - b_%d_%d = 0" % (i, 4 * j + k, i, P[j] * 4 + k)
                Constr.append(temp)


def Permutation(f, Rounds):
    for i in range(Rounds, Rounds + 1):
        for j in range(64):
            Constr.append("a_" + str(i + 1) + "_" + str(j) + " - " + "y_" + str(i) + "_" + str(j) + " = 0")


def ConstraintBySbox(f, Rounds):
    for i in range(Rounds, Rounds + 1):
        for j in range(16):
            for coff in S_T:
                temp = []
                for k in range(4):
                    a = str(coff[k]) + " a_" + str(i) + "_" + str(4 * j + k) + " + "
                    temp.append(a)
                for k in range(3):
                    b = str(coff[k + 4]) + " b_" + str(i) + "_" + str(4 * j + k) + " + "
                    temp.append(b)
                c = str(coff[7]) + " b_" + str(i) + "_" + str(4 * j + 3)
                temp.append(c)
                temp1 = ''.join(temp)
                temp1 = temp1.replace("+ -", "- ")
                s = str(-coff[NUMBER - 1])
                s = s.replace("--", "")
                temp1 += " >= " + s
                Constr.append(temp1)


def gengerate_list(num):
    listA = []
    file2_name = ["MIDORI Paar.txt", "MIDORI BP.txt", "MIDORI XZ.txt"]
    for i in range(4):
        with open(file2_name[num])as f:
            line = f.readline()
            while line:
                line = line.replace("+", "").replace("=", "").split()
                listB = []
                for item in line:
                    if item[0] == "t":
                        listB.append(item[0] + str(int(item[1:]) + (22 * i)))
                    else:
                        listB.append(item[0] + str(int(item[1:]) + (16 * i)))
                listA.append(listB)
                line = f.readline()
    return listA


def matrix(f, Rounds, num2):
    listB = gengerate_list(num2)
    listC = listB.copy()
    for item1 in listB:
        listD = []
        listC.remove(item1)
        if len(listC) > 0:
            listE = reduce(operator.add, listC)
        else:
            listE = []
        for i in range(1, len(item1)):
            a = int(item1[i][1:])
            if item1[i] in listE:
                v0 = get_new_var()
                v1 = get_new_var()
                if item1[i][0] == "x":
                    if len(listX[a]) == 0:
                        listX[a].append(item1[i])
                        listX[a].append(v0)
                        listX[a].append(v1)
                        Constr.append(listX[a][0][0] + "_" + str(Rounds) + "_" + listX[a][0][1:] + " - " + listX[a][1][
                            0] + "_" + str(Rounds) + "_" + listX[a][1][1:]
                                      + " - " + listX[a][2][0] + "_" + str(Rounds) + "_" + listX[a][2][1:] + " = 0")
                        listD.append(listX[a][1])
                        listX[a].remove(listX[a][1])

                    else:
                        listX[a].append(v0)
                        listX[a].append(v1)
                        Constr.append(listX[a][1][0] + "_" + str(Rounds) + "_" + listX[a][1][1:] + " - " + listX[a][2][
                            0] + "_" + str(Rounds) + "_" + listX[a][2][1:]
                                      + " - " + listX[a][3][0] + "_" + str(Rounds) + "_" + listX[a][3][1:] + " = 0")
                        listD.append(listX[a][2])
                        listX[a].remove(listX[a][1])
                        listX[a].remove(listX[a][1])
                elif item1[i][0] == "y":
                    listY[a].append(v0)
                    listY[a].append(v1)
                    Constr.append(
                        listY[a][1][0] + "_" + str(Rounds) + "_" + listY[a][1][1:] + " - " + listY[a][2][0] + "_" + str(
                            Rounds) + "_" + listY[a][2][1:] + " - "
                        + listY[a][3][0] + "_" + str(Rounds) + "_" + listY[a][3][1:] + " = 0")
                    listD.append(listY[a][2])
                    listY[a].remove(listY[a][1])
                    listY[a].remove(listY[a][1])
                else:
                    listT[a].append(v0)
                    listT[a].append(v1)
                    Constr.append(
                        listT[a][1][0] + "_" + str(Rounds) + "_" + listT[a][1][1:] + " - " + listT[a][2][0] + "_" + str(
                            Rounds) + "_" + listT[a][2][1:] + " - "
                        + listT[a][3][0] + "_" + str(Rounds) + "_" + listT[a][3][1:] + " = 0")
                    listD.append(listT[a][2])
                    listT[a].remove(listT[a][1])
                    listT[a].remove(listT[a][1])

            else:
                if item1[i][0] == "x":
                    if len(listX[a]) == 0:
                        listX[a].append(item1[i])
                        listD.append(listX[a][0])
                    else:
                        listD.append(listX[a][1])
                        listX[a].remove(listX[a][1])
                elif item1[i][0] == "t":
                    listD.append(listT[a][1])
                    listT[a].remove(listT[a][1])
                else:
                    listD.append(listY[a][1])
                    listY[a].remove(listY[a][1])

        for i in range(1):
            a = int(item1[i][1:])
            if item1[i][0] == "y":
                if item1[i] in listE:
                    v0 = get_new_var()
                    v1 = get_new_var()
                    listY[a].append(item1[i])
                    listY[a].append(v0)
                    listY[a].append(v1)
                    Constr.append(
                        listY[a][1][0] + "_" + str(Rounds) + "_" + listY[a][1][1:] + " - " + listY[a][0][0] + "_" + str(
                            Rounds) + "_" + listY[a][0][1:] + " - "
                        + listY[a][2][0] + "_" + str(Rounds) + "_" + listY[a][2][1:] + " = 0")
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

        if len(listD) == 3:
            Constr.append(
                listD[0][0] + "_" + str(Rounds) + "_" + listD[0][1:] + " + " + listD[1][0] + "_" + str(Rounds) + "_" +
                listD[1][1:] + " - " +
                listD[2][0] + "_" + str(Rounds) + "_" + listD[2][1:] + " = 0")
        else:
            Constr.append(listD[1][0] + "_" + str(Rounds) + "_" + listD[1][1:] + " - " +
                          listD[0][0] + "_" + str(Rounds) + "_" + listD[0][1:] + " = 0")


def init(f):
    initial = [0] * 64
    for i in range(2):
        initial[i] = 1
    for i in range(3, 64):
        initial[i] = 1
    for i in range(64):
        f.write("a_0_" + str(i) + " = " + str(initial[i]))
        f.write("\n")


def VariableBinary(f, Rounds):
    Var = []
    for i in range(0, Rounds):
        for j in range(64):
            Var.append("a_" + str(i) + "_" + str(j))
            Var.append("b_" + str(i) + "_" + str(j))
            Var.append("x_" + str(i) + "_" + str(j))
            Var.append("y_" + str(i) + "_" + str(j))
        for j in range(672):
            Var.append("u_" + str(i) + "_" + str(j))
    for i in range(Rounds, Rounds + 1):
        for j in range(64):
            Var.append("a_" + str(i) + "_" + str(j))
    f.write("\n".join(Var))


def WriteObjective(f, obj):
    f = open(filename_result, "a")
    f.write("The objective value = %d\n" % (round(obj.getValue())))
    eqn1 = []
    eqn2 = []
    for i in range(0, 64):
        u = obj.getVar(i)
        if u.getAttr("x") != 0:
            eqn1.append(u.getAttr("VarName"))
            eqn2.append(round(u.getAttr("x")))
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
    while counter < 64:
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
                for i in range(64):
                    var = obj.getVar(i)
                    val = round(var.getAttr("x"))
                    if val == 1:
                        set.append(var.getAttr("VarName"))
                        var.ub = 0
                        m.update()
                        counter += 1
                        if counter == 64:
                            print("Integral Distinguisher do NOT exist\n")
                        break
        elif m.Status == 3:
            print("Integral Distinguisher Found!\n")
            break
        else:
            print("Unknown error!")

    f = open(filename_result, "a")
    f.write(str(R) + " rounds\n")
    f.write("Those are the coordinates set to zero: \n")
    for item2 in set:
        f.write(str(item2))
        f.write("\n")
    f.write("\n")
    time_end = time.time()
    f.write(("Time used = " + str(time_end - time_start)) + '\n')
    f.write("\n")
    f.close()


if __name__ == '__main__':
    R = 7
    f.write("Minimize\n")
    ObjectiveFunction(f, R)
    f.write("Subject to\n")
    init(f)
    for i in range(R):
        count = 0
        ConstraintBySbox(f, i)
        ShuffleCell(f, i)
        f.close()
        for j in range(3):
            listX = [[0 for u in range(0)] for v in range(64)]
            listY = [[0 for u in range(0)] for v in range(64)]
            listT = [[0 for u in range(0)] for v in range(88)]
            f = open(file_name, "a")
            matrix(f, i, j)
        Permutation(f, i)
    f.write("\n".join(Constr))
    f.write("\n")
    f = open(file_name, "a")
    f.write("Binary\n")
    VariableBinary(f, R)
    f.write("\n")
    f.write("End\n")
    f.close()
    m = read("demo.lp")
    SolveModel(f, R)
