import operator
from functools import reduce


class Matrix():
    count = 0
    def __init__(self, matrixName, r, num):
        self.matrixName = matrixName
        self.rounds = r
        self.gen_list = self.gengerate_list(num)
        self.listX = [[0 for u in range(0)] for v in range(64)]
        self.listY = [[0 for u in range(0)] for v in range(64)]
        self.listT = [[0 for u in range(0)] for v in range(200)]
        self.constr = []
        self.matrix()

    def get_new_var(self):
        var = 'u' + str(Matrix.count)
        Matrix.count += 1
        return var

    def gengerate_list(self, num):
        listA = []
        file2_name = ['LED Paar.txt', 'LED BP.txt','LED XZ.txt']
        for i in range(4):
            with open(file2_name[num])as f:
                line = f.readline()
                while line:
                    line = line.replace('+', '').replace('=', '').split()
                    listB = []
                    for item in line:
                        if item[0] == 't':
                            listB.append(item[0] + str(int(item[1:]) + (50 * i)))
                        else:
                            listB.append(item[0] + str(int(item[1:]) + (16 * i)))
                    listA.append(listB)
                    line = f.readline()
        return listA

    def matrix(self):
        listC = self.gen_list[:]
        for item1 in self.gen_list:
            listD = []
            listC.remove(item1)
            if len(listC) > 0:
                listE = reduce(operator.add, listC)
            else:
                listE = []
            for i in range(1, len(item1)):
                a = int(item1[i][1:])
                if item1[i] in listE:
                    v0 = self.get_new_var()
                    v1 = self.get_new_var()
                    if item1[i][0] == 'x':
                        if len(self.listX[a]) == 0:
                            self.listX[a].append(item1[i])
                            self.listX[a].append(v0)
                            self.listX[a].append(v1)
                            self.constr.append('ASSERT ' + '~' + self.listX[a][1][
                                0] + '_' + str(self.rounds) + '_' + self.listX[a][1][1:] + ' | ' + '~' +
                                               self.listX[a][2][
                                                   0] + '_' + str(self.rounds) + '_' + self.listX[a][2][
                                                                                       1:] + ' = 0bin1;')
                            self.constr.append(
                                'ASSERT ' + self.listX[a][0][0] + '_' + str(self.rounds) + '_' + self.listX[a][0][
                                                                                                 1:] + ' | ' +
                                self.listX[a][1][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][1][1:] + ' | ' + '~' +
                                self.listX[a][2][0] + '_' + str(self.rounds) + '_' + self.listX[a][2][
                                                                                     1:] + ' = 0bin1;')
                            self.constr.append(
                                'ASSERT ' + self.listX[a][0][0] + '_' + str(self.rounds) + '_' + self.listX[a][0][
                                                                                                 1:] + ' | ' + '~' +
                                self.listX[a][1][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][1][1:] + ' | ' + self.listX[a][2][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][2][1:] + ' = 0bin1;')
                            self.constr.append(
                                'ASSERT ' + '~' + self.listX[a][0][0] + '_' + str(self.rounds) + '_' + self.listX[a][0][
                                                                                                       1:] + ' | ' +
                                self.listX[a][1][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][1][1:] + ' | ' + self.listX[a][2][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][2][1:] + ' = 0bin1;')

                            listD.append(self.listX[a][1])
                            self.listX[a].remove(self.listX[a][1])
                        else:
                            self.listX[a].append(v0)
                            self.listX[a].append(v1)

                            self.constr.append('ASSERT ' + '~' + self.listX[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listX[a][2][1:] + ' | ' + '~' +
                                               self.listX[a][3][
                                                   0] + '_' + str(self.rounds) + '_' +
                                               self.listX[a][3][
                                               1:] + '= 0bin1;')
                            self.constr.append(
                                'ASSERT ' + self.listX[a][1][0] + '_' + str(self.rounds) + '_' + self.listX[a][1][
                                                                                                 1:] + ' | ' +
                                self.listX[a][2][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][2][1:] + ' | ' + '~' +
                                self.listX[a][3][0] + '_' + str(self.rounds) + '_' +
                                self.listX[a][3][
                                1:] + ' = 0bin1;')
                            self.constr.append(
                                'ASSERT ' + self.listX[a][1][0] + '_' + str(self.rounds) + '_' + self.listX[a][1][
                                                                                                 1:] + ' | ' + '~' +
                                self.listX[a][2][
                                    0] + '_' + str(self.rounds) + '_' + self.listX[a][2][1:] + ' | '
                                + self.listX[a][3][0] + '_' + str(self.rounds) + '_' + self.listX[a][3][
                                                                                       1:] + ' = 0bin1;')
                            self.constr.append(
                                'ASSERT ' + '~' + self.listX[a][1][0] + '_' + str(self.rounds) + '_' + self.listX[a][1][
                                                                                                       1:] + ' | ' +
                                self.listX[a][2][0] + '_' + str(self.rounds) + '_' + self.listX[a][2][1:] + ' | ' +
                                self.listX[a][3][0] + '_' + str(self.rounds) + '_' + self.listX[a][3][1:] + ' = 0bin1;')

                            listD.append(self.listX[a][2])
                            self.listX[a].remove(self.listX[a][1])
                            self.listX[a].remove(self.listX[a][1])
                    elif item1[i][0] == 'y':
                        self.listY[a].append(v0)
                        self.listY[a].append(v1)
                        self.constr.append('ASSERT ' + '~' + self.listY[a][2][
                            0] + '_' + str(self.rounds) + '_' + self.listY[a][2][1:] + '|' + '~' + self.listY[a][3][
                                               0] + '_' + str(self.rounds) + '_' + self.listY[a][3][
                                                                                   1:] + '= 0bin1;')
                        self.constr.append(
                            'ASSERT ' + self.listY[a][1][0] + '_' + str(self.rounds) + '_' + self.listY[a][1][
                                                                                             1:] + ' | ' +
                            self.listY[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listY[a][2][1:] + ' | ' + '~' +
                            self.listY[a][3][
                                0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][3][
                            1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + self.listY[a][1][0] + '_' + str(self.rounds) + '_' + self.listY[a][1][
                                                                                             1:] + ' | ' + '~' +
                            self.listY[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listY[a][2][1:] + ' | ' +
                            self.listY[a][3][0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][3][1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + '~' + self.listY[a][1][0] + '_' + str(self.rounds) + '_' + self.listY[a][1][
                                                                                                   1:] + ' | ' +
                            self.listY[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listY[a][2][1:] + ' | ' + self.listY[a][3][
                                0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][3][1:] + ' = 0bin1;')

                        listD.append(self.listY[a][2])
                        self.listY[a].remove(self.listY[a][1])
                        self.listY[a].remove(self.listY[a][1])
                    else:
                        self.listT[a].append(v0)
                        self.listT[a].append(v1)
                        self.constr.append(
                            'ASSERT ' + '~' + self.listT[a][2][0] + '_' + str(self.rounds) + '_' + self.listT[a][2][
                                                                                                   1:] + ' | ' + '~' +
                            self.listT[a][3][0] + '_' + str(self.rounds) + '_' +
                            self.listT[a][3][1:] + '= 0bin1;')
                        self.constr.append(
                            'ASSERT ' + self.listT[a][1][0] + '_' + str(self.rounds) + '_' + self.listT[a][1][
                                                                                             1:] + ' | ' +
                            self.listT[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listT[a][2][1:] + ' | ' + '~' +
                            self.listT[a][3][
                                0] + '_' + str(self.rounds) + '_' +
                            self.listT[a][3][
                            1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + self.listT[a][1][0] + '_' + str(self.rounds) + '_' + self.listT[a][1][
                                                                                             1:] + ' | ' + '~' +
                            self.listT[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listT[a][2][1:] + ' | ' +
                            self.listT[a][3][0] + '_' + str(self.rounds) + '_' +
                            self.listT[a][3][1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + '~' + self.listT[a][1][0] + '_' + str(self.rounds) + '_' + self.listT[a][1][
                                                                                                   1:] + ' | ' +
                            self.listT[a][2][
                                0] + '_' + str(self.rounds) + '_' + self.listT[a][2][1:] + ' | ' + self.listT[a][3][
                                0] + '_' + str(self.rounds) + '_' +
                            self.listT[a][3][1:] + ' = 0bin1;')
                        listD.append(self.listT[a][2])
                        self.listT[a].remove(self.listT[a][1])
                        self.listT[a].remove(self.listT[a][1])


                else:
                    if item1[i][0] == 'x':
                        if len(self.listX[a]) == 0:
                            self.listX[a].append(item1[i])
                            listD.append(self.listX[a][0])
                        else:
                            listD.append(self.listX[a][1])
                            self.listX[a].remove(self.listX[a][1])
                    elif item1[i][0] == 't':
                        listD.append(self.listT[a][1])
                        self.listT[a].remove(self.listT[a][1])
                    else:
                        listD.append(self.listY[a][1])
                        self.listY[a].remove(self.listY[a][1])

            for i in range(1):
                a = int(item1[i][1:])
                if item1[i][0] == 'y':
                    if item1[i] in listE:
                        v0 = self.get_new_var()
                        v1 = self.get_new_var()
                        self.listY[a].append(item1[i])
                        self.listY[a].append(v0)
                        self.listY[a].append(v1)
                        self.constr.append(
                            'ASSERT ' + '~' + self.listY[a][0][0] + '_' + str(self.rounds) + '_' + self.listY[a][0][
                                                                                                   1:] + ' | ' + '~' +
                            self.listY[a][2][0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][2][
                            1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + self.listY[a][1][0] + '_' + str(self.rounds) + '_' + self.listY[a][1][
                                                                                             1:] + ' | ' +
                            self.listY[a][0][
                                0] + '_' + str(self.rounds) + '_' + self.listY[a][0][1:] + ' | ' + '~' +
                            self.listY[a][2][
                                0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][2][
                            1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + self.listY[a][1][0] + '_' + str(self.rounds) + '_' + self.listY[a][1][
                                                                                             1:] + ' | ' + '~' +
                            self.listY[a][0][
                                0] + '_' + str(self.rounds) + '_' + self.listY[a][0][1:] + ' | ' +
                            self.listY[a][2][0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][2][1:] + ' = 0bin1;')
                        self.constr.append(
                            'ASSERT ' + '~' + self.listY[a][1][0] + '_' + str(self.rounds) + '_' + self.listY[a][1][
                                                                                                   1:] + ' | ' +
                            self.listY[a][0][
                                0] + '_' + str(self.rounds) + '_' + self.listY[a][0][1:] + ' | ' + self.listY[a][2][
                                0] + '_' + str(self.rounds) + '_' +
                            self.listY[a][2][1:] + ' = 0bin1;')

                        listD.append(self.listY[a][1])
                        self.listY[a].remove(self.listY[a][1])
                    else:
                        self.listY.append(item1[i])
                        listD.append(item1[i])
                else:
                    if item1[i] in listE:
                        v0 = self.get_new_var()
                        self.listT[a].append(item1[i])
                        self.listT[a].append(v0)
                        listD.append(self.listT[a][1])
                    else:
                        v0 = self.get_new_var()
                        self.listT[a].append(item1[i])
                        self.listT[a].append(v0)
                        listD.append(self.listT[a][1])
                        self.listT[a].remove(self.listT[a][1])
            if len(listD) == 3:
                self.constr.append(
                    'ASSERT ' + '~' + listD[0][0] + '_' + str(self.rounds) + '_' + listD[0][1:] + ' | ' + '~' +
                    listD[1][
                        0] + '_' + str(self.rounds) + '_' + listD[1][
                                                            1:] + ' = 0bin1;')
                self.constr.append(
                    'ASSERT ' + listD[0][0] + '_' + str(self.rounds) + '_' + listD[0][1:] + ' | ' + listD[1][
                        0] + '_' + str(
                        self.rounds) + '_' + listD[1][
                                             1:] + ' | ' + '~' +
                    listD[2][
                        0] + '_' + str(self.rounds) + '_' + listD[2][1:] + ' = 0bin1;')
                self.constr.append(
                    'ASSERT ' + listD[0][0] + '_' + str(self.rounds) + '_' + listD[0][1:] + ' | ' + '~' + listD[1][
                        0] + '_' + str(self.rounds) + '_' + listD[1][
                                                            1:] + ' | ' +
                    listD[2][
                        0] + '_' + str(self.rounds) + '_' + listD[2][1:] + ' = 0bin1;')
                self.constr.append(
                    'ASSERT ' + '~' + listD[0][0] + '_' + str(self.rounds) + '_' + listD[0][1:] + ' | ' + listD[1][
                        0] + '_' + str(self.rounds) + '_' + listD[1][
                                                            1:] + ' | ' +
                    listD[2][
                        0] + '_' + str(self.rounds) + '_' + listD[2][1:] + ' = 0bin1;')

            else:
                self.constr.append('ASSERT ' + listD[1][0] + '_' + str(self.rounds) + '_' + listD[1][1:] + ' - ' +
                                   listD[0][0] + '_' + str(self.rounds) + '_' + listD[0][1:] + ' = 0;')

    def get_declares_asserts(self):
        return self.constr


def main():
    for i in range(64):
        print('x_%d:BITVECTOR(1);' % i)
    for i in range(64):
        print('y_%d:BITVECTOR(1);' % i)
    for i in range(548):
        print('u_%d:BITVECTOR(1);' % i)


if __name__ == '__main__':
    # obj = Matrix('LED', 1, 0)
    L = []
    # main()
    for i in range(1):
        obj = Matrix('LED', 1, i, 0)
        print('\n'.join(obj.get_declares_asserts()))
    for i in range(63):
        print('ASSERT x_%s = 0bin0;' % i)

    for i in range(63, 64):
        print('ASSERT x_%s = 0bin1;' % i)
    for i in range(64):
        L.append('y_%d' % i)
    s = 'ASSERT BVPLUS(10, 0bin000000000@%s' % L[0]
    for i in range(1, 64):
        s += ', 0bin000000000@%s' % L[i]
    s += ') = 0bin0000000001;'
    print(s)
    print('QUERY FALSE;')
