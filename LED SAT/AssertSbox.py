from sboxtrails import *


class Sbox():
    def __init__(self, sboxName, sbox, r, dim, numner_Of_Sbox):
        self.sboxName = sboxName
        self.Rounds = r
        self.numnerOfSbox = numner_Of_Sbox
        self.sboxNames = self.SboxName()
        self.dim = dim
        self.trail = Sboxtrails(sbox)
        self.declares = []
        self.asserts = []

    def SboxName(self):
        sboxNames = []
        for r in range(self.Rounds):
            sboxNameOneRound = []
            for p in range(self.numnerOfSbox):
                sboxNameOneRound.append('%s_%d_%d' % (self.sboxName, r, p))
            sboxNames.append(sboxNameOneRound)
        # print(sboxNames)
        return sboxNames

    def bin(self, num, length):
        return '0bin' + bin(num)[2:].zfill(length)

    def declareSbox(self, r, p):
        trails = self.trail.PrintfDivisionTrails()
        s = '%s:ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % (
            self.sboxNames[r][p], self.dim, self.dim)
        self.declares.append(s)
        for k in range(2 ** self.dim):
            L = []
            s1 = '%s_%d:BITVECTOR(%d);' % (self.sboxNames[r][p], k, self.dim)
            # print('^^^',s1)
            self.declares.append(s1)
            for item in trails:
                if item[0] == k:
                    # print(item)
                    L.append('%s_%d = %s' % (
                        self.sboxNames[r][p],
                        k,
                        self.bin(item[1], self.dim)
                    ))

            self.declares.append('ASSERT %s;' % ' OR '.join(L))

            s2 = 'ASSERT %s[%s] = %s_%d;' % (
                self.sboxNames[r][p],
                self.bin(k, self.dim),
                self.sboxNames[r][p],
                k
            )
            self.asserts.append(s2)

    def build_constrs(self, inVec, outVec, r, p):
        assert len(inVec) == self.dim and len(outVec) == self.dim
        s = 'ASSERT %s = %s[%s];' % (
            '@'.join(outVec),
            self.sboxNames[r][p],
            '@'.join(inVec)
        )
        return s

    def get_assert_declares(self):
        for r in range(self.Rounds):
            for p in range(self.numnerOfSbox):
                self.declareSbox(r, p)
        return self.declares + self.asserts


if __name__ == '__main__':
    sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
    # obj2 = Sboxtrails(sbox)
    # listP = obj2.PrintfDivisionTrails()
    # listP = PrintfDivisionTrails()
    obj = Sbox('sbox', sbox, 1, 4, 16)
    # print(obj.SboxName())
    # print(obj.declareSbox(1, 16))
    # obj.declareSbox(1, 16)
    inVec = ['x0', 'x1', 'x2', 'x3']
    outVec = ['y0', 'y1', 'y2', 'y3']
    print('\n'.join(obj.get_assert_declares()))
    print(obj.build_constrs(inVec, outVec, 0, 15))
