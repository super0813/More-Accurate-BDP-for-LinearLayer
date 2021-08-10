from AssertSbox import *
from Matrix import *


class AES():
    def __init__(self, sboxName, sbox, sboxDim, dim, r, numberOfSbox, matName, num):
        self.Sbox = Sbox(sboxName, sbox, r, sboxDim, numberOfSbox)
        self.dim = dim
        self.round = r
        self.sboxDim = sboxDim
        self.matName = matName
        self.Num = num
        self.constrs = []
        self.variables = self.declareVariables()
        self.afterSboxVariables = self.declareSboxVariables()
        self.declareMatrixVariables()
        self.constrs += self.Sbox.get_assert_declares()
        self.gen_round_constrs()
        self.init()

    def bin(self, num, length):
        return '0bin' + bin(num)[2:].zfill(length)

    def declareVariables(self):
        variables = [[0 for x in range(self.dim)] for x in range(self.round + 1)]
        # print(variables)
        for r in range(self.round + 1):
            for p in range(self.dim):
                s = 'In_X_%d_%d' % (r, p)
                variables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.constrs.append(s)
        return variables

    def declareSboxVariables(self):
        afterSboxVariables = [[0 for x in range(self.dim)] for x in range(self.round)]
        for r in range(self.round):
            for p in range(self.dim):
                s = 'Out_SBOX_%d_%d' % (r, p)
                afterSboxVariables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.constrs.append(s)
        return afterSboxVariables

    def declareMatrixVariables(self):
        for i in range(self.round):
            for p in range(self.dim):
                self.constrs.append('x_%d_%d:BITVECTOR(1);' % (i, p))
            for p in range(self.dim):
                self.constrs.append('y_%d_%d:BITVECTOR(1);' % (i, p))
            for p in range(1668):
                self.constrs.append('u_%d_%d:BITVECTOR(1);' % (i, p))

    def gen_round_constrs(self):
        SR = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
        for r in range(self.round):
            for p in range(int(self.dim / self.sboxDim)):
                self.constrs.append(self.Sbox.build_constrs(self.variables[r][self.sboxDim * p: self.sboxDim * (p + 1)],
                                                            self.afterSboxVariables[r][
                                                            self.sboxDim * p:self.sboxDim * (p + 1)],
                                                            r, p))
        for r in range(self.round):
	    Matrix.count = 0
            for i in range(16):
                for j in range(4):
                    self.constrs.append(
                        'ASSERT x_%d_%d = %s;' % (r, 4 * i + j, self.afterSboxVariables[r][SR[i] * 4 + j]))
	    for i in range(self.Num):
            	m = Matrix(self.matName, r, i)
            	self.constrs += m.get_declares_asserts()
        for r in range(self.round):
            for i in range(64):
                self.constrs.append('ASSERT %s = y_%d_%d;' % (self.variables[r + 1][i], r, i,))

    def init(self):

        for i in range(19):
            self.constrs.append('ASSERT %s = 0bin1;' % self.variables[0][i])
        for i in range(19,20):
            self.constrs.append('ASSERT %s = 0bin0;' % self.variables[0][i])
        for i in range(20,64):
            self.constrs.append('ASSERT %s = 0bin1;' % self.variables[0][i])


        s = 'ASSERT BVPLUS(10, 0bin000000000@%s' % self.variables[self.round][0]
        for i in range(1, 64):
            s += ', 0bin000000000@%s' % self.variables[self.round][i]
        s += ') = 0bin0000000001;'
        self.constrs.append(s)
        self.constrs.append('QUERY FALSE;')

    def getConstrs(self):
        return self.constrs


if __name__ == '__main__':
    sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
    obj = AES('LEDSBOX', sbox, 4, 64, 7, 16, 'LEDmatrix', 3)

    print('\n'.join(obj.getConstrs()))
