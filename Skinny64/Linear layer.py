from gurobipy import *
import operator
from functools import reduce
import time

filename_result = "result2.txt"
file_name = "demo2.lp"
f = open(file_name, "w")
Constr = []

def get_new_var():
    global count
    var = "u" + str(count)
    count += 1
    return var


def ObjectiveFunction(f):
    eqn = []
    for j in range(16):
        eqn.append("y_" + str(j))
    temp = " + ".join(eqn)
    f.write(temp)
    f.write("\n")


def gengerate_list(num):
    listA = []
    file2_name = ["Skinny BP.txt"]
    for i in range(1):
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


def matrix(f, num2):
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
                        Constr.append(listX[a][0][0] + "_" + listX[a][0][1:] + " - " + listX[a][1][
                            0] + "_" + listX[a][1][1:]
                                + " - " + listX[a][2][0] + "_" + listX[a][2][1:] + " = 0")
                        listD.append(listX[a][1])
                        listX[a].remove(listX[a][1])

                    else:
                        listX[a].append(v0)
                        listX[a].append(v1)
                        Constr.append(listX[a][1][0] + "_" + listX[a][1][1:] + " - " + listX[a][2][
                            0] + "_" + listX[a][2][1:]
                                + " - " + listX[a][3][0] + "_" + listX[a][3][1:] + " = 0")
                        listD.append(listX[a][2])
                        listX[a].remove(listX[a][1])
                        listX[a].remove(listX[a][1])
                elif item1[i][0] == "y":
                    listY[a].append(v0)
                    listY[a].append(v1)
                    Constr.append(
                        listY[a][1][0] + "_" + listY[a][1][1:] + " - " + listY[a][2][0] + "_" + listY[a][2][1:] + " - "
                        + listY[a][3][0] + "_" + listY[a][3][1:] + " = 0")
                    listD.append(listY[a][2])
                    listY[a].remove(listY[a][1])
                    listY[a].remove(listY[a][1])
                else:
                    listT[a].append(v0)
                    listT[a].append(v1)
                    Constr.append(
                        listT[a][1][0] + "_" + listT[a][1][1:] + " - " + listT[a][2][0] + "_" + listT[a][2][1:] + " - "
                        + listT[a][3][0] + "_" + listT[a][3][1:] + " = 0")
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
                        listY[a][1][0] + "_" + listY[a][1][1:] + " - " + listY[a][0][0] + "_" + listY[a][0][1:] + " - "
                        + listY[a][2][0] + "_" + listY[a][2][1:] + " = 0")
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
            Constr.append(listD[0][0] + "_" + listD[0][1:] + " + " + listD[1][0] + "_" +
                    listD[1][1:] + " - " +
                    listD[2][0] + "_" + listD[2][1:] + " = 0")
        else:
            Constr.append(listD[1][0] + "_" + listD[1][1:] + " - " +
                    listD[0][0] + "_" + listD[0][1:] + " = 0")


def init(f, w):
    for j in range(15):
        f.write("x_" + str(j) + " + ")
    f.write("x_" + str(15) + ' = ' + str(w) + "\n")
    for j in range(15):
        f.write("y_" + str(j) + " + ")
    f.write("y_" + str(15) + ' = ' + str(w) + "\n")


def VariableBinary(f):
    for j in range(16):
        f.write("x_" + str(j) + "\n")
        f.write("y_" + str(j) + "\n")
    for j in range(24):
        f.write("u_" + str(j) + "\n")


if __name__ == '__main__':
    total = []
    for w in range(3):
        s = set()
        f = open(file_name, "w")
        f.write("Minimize\n")
        ObjectiveFunction(f)
        f.write("Subject to\n")
        init(f, w)
        count = 0
        f.close()
        for j in range(1):
            listX = [[0 for u in range(0)] for v in range(64)]
            listY = [[0 for u in range(0)] for v in range(64)]
            listT = [[0 for u in range(0)] for v in range(88)]
            f = open(file_name, "a")
            matrix(f, j)
        f.write("\n".join(Constr))
        f = open(file_name, "a")
        f.write("\n")
        f.write("Binary\n")
        VariableBinary(f)
        f.write("End\n")
        f.close()
        m = read("demo2.lp")
        m.Params.PoolSearchMode = 2
        m.Params.PoolSolutions = 200000000
        m.optimize()
        Count = m.SolCount
        print("所有的可行解:", Count)
        f.close()
        for e in range(Count):
            solutions = ""
            m.Params.SolutionNumber = e
            for i in range(32):
                solutions += str(round(m.getAttr("Xn")[i]))
            s.add(solutions)
        for item in s:
            f = open(filename_result, "a")
            f.write(item)
            f.write("\n")
        print("可分路径条数为:", len(s))
        total.append(len(s))
        print(total)
